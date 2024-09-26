#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=broad-except
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=multiple-statements
# pylint: disable=too-many-lines

#-------------------------------------------------------------------------------

'''
This program calculates:
    * sample genotypes of SNPs
    * linkage disequilibrium between each pair of SNPs
        (Ragsdale, Gravel - 2020 - Unbiased Estimation of Linkage Disequilibrium from Unphased Data - DOI: 10.1093/molbev/msz265)
    * sample kinship
        (Goudet, Kay, Weir - 2018 - How to estimate kinship - DOI: 10.1111/mec.14833)
Multiallelic loci and other types of variants are not considered.

This software has been developed by:

    GI en Especies Leñosas (WooSp)
    Dpto. Sistemas y Recursos Naturales
    ETSI Montes, Forestal y del Medio Natural
    Universidad Politecnica de Madrid
    https://github.com/ggfhf/

Licence: GNU General Public Licence Version 3.
'''

#-------------------------------------------------------------------------------

import argparse
import gzip
import os
import sys
import threading

from threading import Semaphore

import genlib
import sqllib

#-------------------------------------------------------------------------------

def main():
    '''
    Main line of the program.
    '''

    # check the operating system
    genlib.check_os()

    # get and check the arguments
    parser = build_parser()
    args = parser.parse_args()
    check_args(args)

    # connect to the genotype database
    conn = sqllib.connect_database(args.genotype_database, check_same_thread=False)

    # calculate genotype data
    calculate_genotype_data(conn, args.threads_num, args.vcf_file, args.tvi_list)

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program calculates genotype data: sample genotypes of SNPs, linkage disequilibrium\n' \
        'between each pair of SNPs and sample kinship.'
    text = f'{genlib.get_app_long_name()} v{genlib.get_app_version()} - {os.path.basename(__file__)}\n\n{description}\n'
    usage = f'\r{text.ljust(len("usage:"))}\nUsage: {os.path.basename(__file__)} arguments'
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'    #pylint: disable=protected-access
    parser.add_argument('--threads', dest='threads_num', help='Number of threads (mandatory).')
    parser.add_argument('--gtdb', dest='genotype_database', help='Path of the genotype database (mandatory).')
    parser.add_argument('--vcf', dest='vcf_file', help='Path of the input VCF file (mandatory).')
    parser.add_argument('--verbose', dest='verbose', help=f'Additional job status info during the run: {genlib.get_verbose_code_list_text()}; default: {genlib.Const.DEFAULT_VERBOSE}.')
    parser.add_argument('--trace', dest='trace', help=f'Additional info useful to the developer team: {genlib.get_trace_code_list_text()}; default: {genlib.Const.DEFAULT_TRACE}.')
    parser.add_argument('--tvi', dest='tvi_list', help='Variant identification list to trace with format seq_id_1-pos_1,seq_id_2-pos_2,...,seq_id_n-pos_n or NONE; default: NONE.')

    # return the paser
    return parser

#-------------------------------------------------------------------------------

def check_args(args):
    '''
    Check the input arguments.
    '''

    # initialize the control variable
    OK = True

    # check "threads_num"
    if args.threads_num is None:
        genlib.Message.print('error', '*** The number of threads is not indicated in the input arguments.')
        OK = False
    elif not genlib.check_int(args.threads_num, minimum=1):
        genlib.Message.print('error', 'The number of threads has to be an integer number greater than or equal to 1.')
        OK = False
    else:
        args.threads_num = int(args.threads_num)

    # check "genotype_database"
    if args.genotype_database is None:
        genlib.Message.print('error', '*** The genotype database is not indicated in the input arguments.')
        OK = False

    # check "vcf_file"
    if args.vcf_file is None:
        genlib.Message.print('error', '*** The VCF file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.vcf_file):
        genlib.Message.print('error', f'*** The file {args.vcf_file} does not exist.')
        OK = False

    # check "verbose"
    if args.verbose is None:
        args.verbose = genlib.Const.DEFAULT_VERBOSE
    elif not genlib.check_code(args.verbose, genlib.get_verbose_code_list(), case_sensitive=False):
        genlib.Message.print('error', f'*** verbose has to be {genlib.get_verbose_code_list_text()}.')
        OK = False
    if args.verbose.upper() == 'Y':
        genlib.Message.set_verbose_status(True)

    # check "trace"
    if args.trace is None:
        args.trace = genlib.Const.DEFAULT_TRACE
    elif not genlib.check_code(args.trace, genlib.get_trace_code_list(), case_sensitive=False):
        genlib.Message.print('error', f'*** trace has to be {genlib.get_trace_code_list_text()}.')
        OK = False
    if args.trace.upper() == 'Y':
        genlib.Message.set_trace_status(True)

    # check "tvi_list"
    if args.tvi_list is None or args.tvi_list == 'NONE':
        args.tvi_list = []
    else:
        args.tvi_list = genlib.split_literal_to_string_list(args.tvi_list)

    # if there are errors, exit with exception
    if not OK:
        raise genlib.ProgramException('', 'P001')

#-------------------------------------------------------------------------------

def calculate_genotype_data(conn, threads_num, vcf_file, tvi_list):
    '''
    Calculate the following genotype data:
        * sample genotypes of SNPs
        * linkage disequilibrium between each pair of SNPs
          (Ragsdale, Gravel - 2020 - Unbiased Estimation of Linkage Disequilibrium from Unphased Data - DOI: 10.1093/molbev/msz265)
        * sample kinship
          (Goudet, Kay, Weir - 2018 - How to estimate kinship - DOI: 10.1111/mec.14833)
    Multiallelic loci and other types of variants are not considered.
    '''

    # get the number of CPUs in the system
    cpus_num = os.cpu_count()

    # set the mximum number of threads to be used
    if cpus_num is None:
        max_threads_num = threads_num
        genlib.Message.print('info', f'CPUs number in the system is undetermed. The process will use {threads_num} threads.\n')
    else:
        if cpus_num >=  threads_num:
            max_threads_num = threads_num
        else:
            max_threads_num = cpus_num
        genlib.Message.print('verbose', f'CPUs in the system: {cpus_num}.  The process will use {max_threads_num} threads.\n')

    # initialize the sample lis, sample number and label dict
    sample_list = []
    sample_number = 0
    label_dict = {}

    # initialize the kinship dictionary
    kinship_dict = genlib.NestedDefaultDict()

    # drop the table "vcf_snps" (if it exists)
    genlib.Message.print('verbose', 'Droping the table "vcf_snps" ...\n')
    sqllib.drop_vcf_snps(conn)
    genlib.Message.print('verbose', 'The table is droped.\n')

    # create the table "vcf_snps"
    genlib.Message.print('verbose', 'Creating the table "vcf_snps" ...\n')
    sqllib.create_vcf_snps(conn)
    genlib.Message.print('verbose', 'The table is created.\n')

    # drop the table "vcf_linkage_disequilibrium" (if it exists)
    genlib.Message.print('verbose', 'Droping the table "vcf_linkage_disequilibrium" ...\n')
    sqllib.drop_vcf_linkage_disequilibrium(conn)
    genlib.Message.print('verbose', 'The table is droped.\n')

    # create the table "vcf_linkage_disequilibrium"
    genlib.Message.print('verbose', 'Creating the table "vcf_linkage_disequilibrium" ...\n')
    sqllib.create_vcf_linkage_disequilibrium(conn)
    genlib.Message.print('verbose', 'The table is created.\n')

    # drop the table "vcf_kinship" (if it exists)
    genlib.Message.print('verbose', 'Droping the table "vcf_kinship" ...\n')
    sqllib.drop_vcf_kinship(conn)
    genlib.Message.print('verbose', 'The table is droped.\n')

    # create the table "vcf_kinship"
    genlib.Message.print('verbose', 'Creating the table "vcf_kinship" ...\n')
    sqllib.create_vcf_kinship(conn)
    genlib.Message.print('verbose', 'The table is created.\n')

    genlib.Message.print('verbose', f'Processing SNPs of the file {vcf_file} ...\n')
    genlib.Message.print('verbose', 'Reading the VCF file:\n')

    # open the input VCF file
    if vcf_file.endswith('.gz'):
        try:
            vcf_file_id = gzip.open(vcf_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise genlib.ProgramException(e, 'F002', vcf_file)
    else:
        try:
            vcf_file_id = open(vcf_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise genlib.ProgramException(e, 'F001', vcf_file)

    # initialize counters
    input_record_counter = 0
    total_variant_counter = 0

    # read the first record of input VCF file
    (record, _, data_dict) = genlib.read_vcf_file(vcf_file_id, sample_number=0, check_sample_number=False)

    # while there are records in the VCF file to check
    while record != '':

        # process metadata records
        while record != '' and record.startswith('##'):

            # add 1 to the input record counter
            input_record_counter += 1

            # print the counters
            genlib.Message.print('verbose', f'\rRecords ... {input_record_counter:8d} - Variants ... {total_variant_counter:8d}')

            # read the next record of the input VCF file
            (record, _, data_dict) = genlib.read_vcf_file(vcf_file_id, sample_number=0, check_sample_number=False)

        # process the column description record
        if record.startswith('#CHROM'):

            # add 1 to the input record counter
            input_record_counter += 1

            # get the record data list
            record_data_list = data_dict['record_data_list']

            # build the sample list and label dictionary
            for i in range(9, len(record_data_list)):
                sample_list.append(os.path.basename(record_data_list[i]))
                label_dict[f'{i - 9:04d}'] = i - 9

            # set the samples number
            sample_number = len(sample_list)
            genlib.Message.print('trace', f'sample_number: {sample_number}')

            # set 0 in the values of the kinship dictionary
            for i in range(sample_number):
                for j in range(i + 1, sample_number):
                    kinship_dict[i][j]['rbeta_summation'] = 0
                    kinship_dict[i][j]['rw_numerator_summation'] = 0
                    kinship_dict[i][j]['rw_denominator_summation'] = 0
                    kinship_dict[i][j]['ru_summation'] = 0
                    kinship_dict[i][j]['ru_l'] = 0

            # print the counters
            genlib.Message.print('verbose', f'\rRecords ... {input_record_counter:8d} - Variants ... {total_variant_counter:8d}')

            # read the next record of the input VCF file
            (record, _, data_dict) = genlib.read_vcf_file(vcf_file_id, sample_number=0, check_sample_number=False)

        # process variant record
        while record != '' and not record.startswith('##') and not record.startswith('#CHROM'):

            # add 1 to the input record counter
            input_record_counter += 1

            # add 1 to the total variant counter
            total_variant_counter += 1

            # set the variant identification
            variant_id = f'{data_dict["chrom"]}-{data_dict["pos"]}'

            # get the reference allele and alternative alleles (field ALT)
            reference_allele = data_dict['ref']
            alternative_alleles = data_dict['alt']

            # build the alternative alleles list from field ALT
            alternative_allele_list = alternative_alleles.split(',')

            # check if the variant has more than one alternative allele
            if len(alternative_allele_list) > 1:
                raise genlib.ProgramException('', 'L021', variant_id) from None

            # get the position of the genotype (subfield GT) in the field FORMAT
            format_subfield_list = data_dict['format'].upper().split(':')
            try:
                gt_position = format_subfield_list.index('GT')
            except Exception as e:
                raise genlib.ProgramException(e, 'L002', 'GT', data_dict['chrom'], data_dict['pos'])

            # build the list of sample genotypes of a variant
            sample_data_list = []
            sample_gt_list = []
            for i in range(sample_number):
                sample_data_list.append(data_dict['sample_list'][i].split(':'))
                sample_gt_list.append(sample_data_list[i][gt_position])

            # build the lists of sample genotypes using binary numbers and samples with missing data
            pseudobinary_sample_gt_list = []
            gt_00 = 0
            gt_01 = 0
            gt_11 = 0
            sample_withmd_list = []
            for i in range(sample_number):
                # build the lists of the left and right side of sample genotypes of a variant
                sep = '/'
                sep_pos = sample_gt_list[i].find(sep)
                if sep_pos == -1:
                    sep = '|'
                    sep_pos = sample_gt_list[i].find(sep)
                if sep_pos == -1:
                    raise genlib.ProgramException('', 'L003', 'GT', data_dict['chrom'], data_dict['pos'])
                sample_gt_left = sample_gt_list[i][:sep_pos]
                sample_gt_right = sample_gt_list[i][sep_pos+1:]

                if sample_gt_left == '0' and sample_gt_right == '0':
                    gt_00 += 1
                    # 0b00 -> 0
                    pseudobinary_sample_gt_list.append(0)
                elif sample_gt_left == '0' and sample_gt_right == '1' or sample_gt_left == '1' and sample_gt_right == '0':
                    gt_01 += 1
                    # 0b01 -> 1
                    pseudobinary_sample_gt_list.append(1)
                elif sample_gt_left == '1' and sample_gt_right == '1':
                    gt_11 += 1
                    # 0b11 -> 3
                    pseudobinary_sample_gt_list.append(3)
                else:
                    # 0b111 -> 7
                    pseudobinary_sample_gt_list.append(7)
                    sample_withmd_list.append(i)

            # update the kinship dictionary adding data of the samples i and j in the summations
            # used to the calculation of rbeta, rw (weighted estimator) y ru (unweighted average estimator)
            #
            #    rbeta:
            #        (1 + (Xi - 1) * (Xj - 1)) / 2 ---> rbeta_summation
            #
            #    rw:
            #        (Xi - 2 * p) * (Xj - 2 * p) ---> rw_numerator_summation
            #        2 * p * (1 - p) ---> rw_denominator_summation
            #
            #    ru:
            #        (Xi - 2 * p) * (Xj - 2 * p) / (2 * p * (1 - p)) ---> ru_summation
            #
            # where Xi are Xj are the dosage of reference allele for samples i and j respectivily
            # and p is the frecuence of reference allele in the current variant
            #
            # (no update is done when there is missing data in samples i or j, or p value is 0 or 1 when rw and ru)
            summation_summation_mij = 0
            p = (gt_00 * 2 + gt_01) / (sample_number * 2)
            for i in range(sample_number):
                Xi = 0
                # 0b00 -> 0
                if pseudobinary_sample_gt_list[i] == 0:
                    Xi = 2
                # 0b01 -> 1
                elif pseudobinary_sample_gt_list[i] == 1:
                    Xi = 1
                for j in range(i + 1, sample_number):
                    Xj = 0
                    # 0b00 -> 0
                    if pseudobinary_sample_gt_list[j] == 0:
                        Xj = 2
                    # 0b01 -> 1
                    elif pseudobinary_sample_gt_list[j] == 1:
                        Xj = 1
                    # 0b111 -> 7
                    if pseudobinary_sample_gt_list[i] != 7 and pseudobinary_sample_gt_list[j] != 7 and p not in [0, 1]:
                        mij_item = (1 + (Xi - 1) * (Xj - 1)) / 2
                        kinship_dict[i][j]['rbeta_summation'] += mij_item
                        summation_summation_mij += mij_item
                        if p not in [0, 1]:
                            kinship_dict[i][j]['rw_numerator_summation'] += (Xi - 2 * p) * (Xj - 2 * p)
                            kinship_dict[i][j]['rw_denominator_summation'] += 2 * p * (1 - p)
                            kinship_dict[i][j]['ru_summation'] += (Xi - 2 * p) * (Xj - 2 * p) / (2 * p * (1 - p))
                            kinship_dict[i][j]['ru_l'] += 1

            # save SNP data into table "vcf_snps" if there are more than one genotype
            if gt_00 != sample_number and gt_01 != sample_number and gt_11 != sample_number:
                snp_row_dict = {}
                snp_row_dict['variant_id'] = variant_id
                snp_row_dict['ref'] = reference_allele
                snp_row_dict['alt'] = alternative_allele_list[0]
                snp_row_dict['sample_gt_list'] = ','.join(str(x) for x in pseudobinary_sample_gt_list)
                snp_row_dict['sample_withmd_list'] = ','.join(str(x) for x in sample_withmd_list)
                sqllib.insert_vcf_snps_row(conn, snp_row_dict)

            # print the counters
            genlib.Message.print('verbose', f'\rRecords ... {input_record_counter:8d} - Variants ... {total_variant_counter:8d}')

            # read the next record of the VCF file to check
            (record, _, data_dict) = genlib.read_vcf_file(vcf_file_id, sample_number=0, check_sample_number=False)

    genlib.Message.print('verbose', '\n')

    # close input VCF file
    vcf_file_id.close()

    genlib.Message.print('verbose', 'SNPs are processed.\n')

    # create the index "vcf_snps_index" on the table "vcf_snps"
    genlib.Message.print('verbose', 'Creating the index on the table "vcf_snps" ...\n')
    sqllib.create_vcf_snps_index(conn)
    genlib.Message.print('verbose', 'The index is created.\n')

    # save changes into genotype database
    genlib.Message.print('verbose', 'Saving changes into genotype database ...\n')
    conn.commit()
    genlib.Message.print('verbose', 'Changes are saved.\n')

    # save kinship calculations into the table "vcf_kinship"
    genlib.Message.print('verbose', 'Saving kinship calculations into the table "vcf_kinship" ...\n')
    ms = summation_summation_mij * 2 / (sample_number * (sample_number - 1))
    for i in range(sample_number):
        for j in range(i + 1, sample_number):
            rbeta = (kinship_dict[i][j]['rbeta_summation'] - ms) / (1 - ms)
            try:
                rw = kinship_dict[i][j]['rw_numerator_summation'] / kinship_dict[i][j]['rw_denominator_summation']
                ru = kinship_dict[i][j]['ru_summation'] / kinship_dict[i][j]['ru_l']
            except ZeroDivisionError as e:
                genlib.Message.print('info', '*** WARNING: ZeroDivisionError calculating kinship data')
                genlib.Message.print('info', f'between samples {sample_list[i]} & {sample_list[j]}')
                genlib.Message.print('info', 'due to all variants have missing data in at least one of the two samples.')
                rw = -999
                ru = -999
            kinship_row_dict = {}
            kinship_row_dict['individual_i'] = i
            kinship_row_dict['individual_j'] = j
            kinship_row_dict['rbeta'] = rbeta
            kinship_row_dict['rw'] = rw
            kinship_row_dict['ru'] = ru
            sqllib.insert_vcf_kinship_row(conn, kinship_row_dict)
    genlib.Message.print('verbose', 'Kinship calculations are saved.\n')

    # create the index "vcf_kinship_index" on the table "vcf_kinship"
    genlib.Message.print('verbose', 'Creating the index on the table "vcf_kinship" ...\n')
    sqllib.create_vcf_kinship_index(conn)
    genlib.Message.print('verbose', 'The index is created.\n')

    # save changes into genotype database
    genlib.Message.print('verbose', 'Saving changes into genotype database ...\n')
    conn.commit()
    genlib.Message.print('verbose', 'Changes are saved.\n')

    genlib.Message.print('verbose', 'Calculating the linkage disequilibrium ...\n')

    # get the SNPs identification lists from the table  "vcf_snps"
    snp_id_list_1 = sorted(sqllib.get_snp_ids_wmd_list(conn))
    snp_id_list_2 = sorted(sqllib.get_snp_ids_list(conn))

    # initialice the counter and total of SNPs
    snps_counter = 0
    snps_total = len(snp_id_list_1)

    # create the semaphore to control databases accesses
    semaphore = Semaphore(1)

    # calculate the linkage disequilibrium between each pair of SNPs
    while snps_counter < snps_total:

        # initialize working threads number
        w_threads_num = 0

        # initialize the list of SNP identifications in the group
        group_snp_id_list_1 = []

        while snps_counter < snps_total and w_threads_num < max_threads_num:

            # add 1 to the working threads number
            w_threads_num += 1

            # add the SNP identification to the list of SNP identifications in the group
            group_snp_id_list_1.append(snp_id_list_1[snps_counter])

            # add 1 to the SNPs counter
            snps_counter += 1

        # create and start threads
        threads_list = []
        for thread_id in range(w_threads_num):
            threads_list.append(threading.Thread(target=calculate_snp_linkage_disequilibrium, args=[conn, semaphore, sample_number, group_snp_id_list_1[thread_id], snp_id_list_2]))
            threads_list[thread_id].start()

        # wait until all threads terminate
        for thread_id in range(w_threads_num):
            threads_list[thread_id].join()

        genlib.Message.print('verbose', f'\r... SNPs counter: {snps_counter}/{snps_total} ...              ')

    genlib.Message.print('verbose', '\n')
    genlib.Message.print('verbose', 'The linkage disequilibrium is calculated.\n')

    # create the index "vcf_linkage_disequilibrium_index" on the table "vcf_linkage_disequilibrium"
    genlib.Message.print('verbose', 'Creating the index on the table "vcf_linkage_disequilibrium" ...\n')
    sqllib.create_vcf_linkage_disequilibrium_index(conn)
    genlib.Message.print('verbose', 'The index is created.\n')

    # save changes into genotype database
    genlib.Message.print('verbose', 'Saving changes into genotype database ...\n')
    conn.commit()
    genlib.Message.print('verbose', 'Changes are saved.\n')

#-------------------------------------------------------------------------------

def calculate_snp_linkage_disequilibrium(conn, semaphore, sample_number, snp_id_1, snp_id_list_2):
    '''
    Calculate the linkage disequilibrium of a SNP.
    '''

    # get data of the first SNP from table "vcf_snps"
    semaphore.acquire()
    snp_data_dict_1 = sqllib.get_snp_data_dict(conn, snp_id_1)
    semaphore.release()

    # get the the list of sample genotypes using pseudo binary numbers
    pseudobinary_sample_gt_list_1 = genlib.split_literal_to_integer_list(snp_data_dict_1['sample_gt_list'])

    # get the list of the remained SNP identification
    w_snp_id_list_2 = snp_id_list_2.copy()
    w_snp_id_list_2.remove(snp_id_1)

    # calculate the linkage disequilibrium
    for snp_id_2 in w_snp_id_list_2:

        # get data of the first SNP from table "vcf_snps"
        semaphore.acquire()
        snp_data_dict_2 = sqllib.get_snp_data_dict(conn, snp_id_2)
        semaphore.release()

        # get the the list of sample genotypes using pseudo binary numbers
        pseudobinary_sample_gt_list_2 = genlib.split_literal_to_integer_list(snp_data_dict_2['sample_gt_list'])

        # calculate the observed genotype counts and allele frequencies
        #
        #  ri: reference allele of SNPi; ai: alternative allele of SNPi; ni: count of observed genotype pair i
        #         r2-r2 r2-a2 a2-a2
        #        +-----------------
        #  r1-r1 |  n1    n2    n3
        #  r1-a1 |  n4    n5    n6
        #  a1-a1 |  n7    n8    n9
        #
        # rfi: reference allele frequency of SNP i; afi: alternative allele frequency of SNP i
        #
        # (samples with missing data '0b111' are not considered!!!)
        n = n1 = n2 = n3 = n4 = n5 = n6 = n7 = n8 = n9 = 0
        rf1 = af1 = rf2 = af2 = 0
        for i in range(sample_number):
            if pseudobinary_sample_gt_list_1[i] == 0 and pseudobinary_sample_gt_list_2[i] == 0:
                n += 1
                n1 += 1
                rf1 += 2
                rf2 += 2
            elif pseudobinary_sample_gt_list_1[i] == 0 and pseudobinary_sample_gt_list_2[i] == 1:
                n += 1
                n2 += 1
                rf1 += 2
                rf2 += 1
                af2 += 1
            elif pseudobinary_sample_gt_list_1[i] == 0 and pseudobinary_sample_gt_list_2[i] == 3:
                n += 1
                n3 += 1
                rf1 += 2
                af2 += 2
            elif pseudobinary_sample_gt_list_1[i] == 1 and pseudobinary_sample_gt_list_2[i] == 0:
                n += 1
                n4 += 1
                rf1 += 1
                af1 += 1
                rf2 += 2
            elif pseudobinary_sample_gt_list_1[i] == 1 and pseudobinary_sample_gt_list_2[i] == 1:
                n += 1
                n5 += 1
                rf1 += 1
                af1 += 1
                rf2 += 1
                af2 += 1
            elif pseudobinary_sample_gt_list_1[i] == 1 and pseudobinary_sample_gt_list_2[i] == 3:
                n += 1
                n6 += 1
                rf1 += 1
                af1 += 1
                af2 += 2
            elif pseudobinary_sample_gt_list_1[i] == 3 and pseudobinary_sample_gt_list_2[i] == 0:
                n += 1
                n7 += 1
                af1 += 2
                rf2 += 2
            elif pseudobinary_sample_gt_list_1[i] == 3 and pseudobinary_sample_gt_list_2[i] == 1:
                n += 1
                n8 += 1
                af1 += 2
                rf2 += 1
                af2 += 1
            elif pseudobinary_sample_gt_list_1[i] == 3 and pseudobinary_sample_gt_list_2[i] == 3:
                n += 1
                n9 += 1
                af1 += 2
                af2 += 2

        # calculate the unbiased estimator for the covariance of alleles co-occurring on a haplotype
        # (Ragsdale, Gravel - 2020 - Unbiased Estimation of Linkage Disequilibrium from Unphased Data)
        dhat = ((n1 + n2/2 + n4/2 + n5/4) * (n5/4 + n6/2 + n8/2 + n9) - (n2/2 + n3 + n5/4 + n6/2) * (n4/2 + n5/4 + n7 + n8/2)) / (n * (n - 1))

        # calculate the squared correlation
        try:
            rf1 = rf1 / (n * 2)
            af1 = af1 / (n * 2)
            rf2 = rf2 / (n * 2)
            af2 = af2 / (n * 2)
            r2 = (dhat ** 2) / (rf1 * af1 * rf2 * af2)
        except ZeroDivisionError:
            r2 = -999
            genlib.Message.print('info', '*** WARNING: LD r^2 is not calculated because a ZeroDivisionError exception was raised.')
            genlib.Message.print('info', f'snp_id_1: {snp_id_1} - snp_id_2: {snp_id_2}')
            genlib.Message.print('info', f'n: {n} - n1: {n1} - n2: {n2} - n3: {n3} - n4: {n4} - n5: {n5} - n6: {n6} - n7: {n7} - n8: {n8} - n9: {n9}')
            genlib.Message.print('info', f'rf1: {rf1} - af1: {af1} - rf2: {rf2} - af2: {af2}')

        # save linkage disequilibrium data into the table "vcf_linkage_disequilibrium"
        ld_row_dict = {}
        ld_row_dict['snp_id_1'] = snp_id_1
        ld_row_dict['snp_id_2'] = snp_id_2
        ld_row_dict['dhat'] = dhat
        ld_row_dict['r2'] = r2
        ld_row_dict['sample_withmd_list_2'] = snp_data_dict_2['sample_withmd_list']
        semaphore.acquire()
        sqllib.insert_vcf_linkage_disequilibrium_row(conn, ld_row_dict)
        semaphore.release()

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
    sys.exit(0)

#-------------------------------------------------------------------------------
