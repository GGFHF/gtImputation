#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=broad-except
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=multiple-statements
# pylint: disable=too-many-lines

#-------------------------------------------------------------------------------

'''
This software has been developed by:

    GI en Desarrollo de Especies y Comunidades Leñosas (WooSp)
    Dpto. Sistemas y Recursos Naturales
    ETSI Montes, Forestal y del Medio Natural
    Universidad Politecnica de Madrid
    https://github.com/ggfhf/

Licence: GNU General Public Licence Version 3.
'''

#-------------------------------------------------------------------------------

import math
import sqlite3
import sys

import genlib

#-------------------------------------------------------------------------------

def connect_database(database_path, check_same_thread=True):
    '''
    Connect to the database.
    '''

    # connet to the database
    try:
        conn = sqlite3.connect(database_path, check_same_thread=check_same_thread)
    except Exception as e:
        raise genlib.ProgramException(e, 'B001', database_path)

    # return the connection
    return conn

#-------------------------------------------------------------------------------
# table "vcf_snps"
#-------------------------------------------------------------------------------

def drop_vcf_snps(conn):
    '''
    Drop the table "vcf_snps" (if it exists)
    '''

    sentence = '''
               DROP TABLE IF EXISTS vcf_snps;
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

#-------------------------------------------------------------------------------

def create_vcf_snps(conn):
    '''
    Create the table "vcf_snps".
    '''

    sentence = '''
               CREATE TABLE vcf_snps (
                   variant_id         TEXT NOT NULL,
                   ref                TEXT NOT NULL,
                   alt                TEXT NOT NULL,
                   sample_gt_list     TEXT NOT NULL,
                   sample_withmd_list TEXT);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

#-------------------------------------------------------------------------------

def create_vcf_snps_index(conn):
    '''
    Create the unique index "vcf_snps_index" with the column "variant_id" on the table "vcf_snps"
    '''

    sentence = '''
               CREATE UNIQUE INDEX vcf_snps_index
                   ON vcf_snps (variant_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

#-------------------------------------------------------------------------------

def insert_vcf_snps_row(conn, row_dict):
    '''
    Insert a row into table "vcf_snps"
    '''

    sentence = f'''
                INSERT INTO vcf_snps
                    (variant_id, ref, alt, sample_gt_list, sample_withmd_list)
                    VALUES ('{row_dict["variant_id"]}', '{row_dict["ref"]}', '{row_dict["alt"]}', '{row_dict["sample_gt_list"]}', '{row_dict["sample_withmd_list"]}')
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

#-------------------------------------------------------------------------------

def check_vcf_snps(conn):
    '''
    Check if table "vcf_snps" exists and if there are rows.
    '''


    # initialize the control variable
    control = 0

    # check if table "vcf_snps" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'vcf_snps'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "vcf_snps" exists
    if control == 1:

        # select the row number
        sentence = '''
                   SELECT EXISTS
                       (SELECT 1
                           FROM vcf_snps
                           LIMIT 1);
                   '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise genlib.ProgramException(e, 'B002', sentence, conn)

        for row in rows:
            control = int(row[0])
            break

    # return the control variable
    return control

#-------------------------------------------------------------------------------

def get_snp_data_dict(conn, snp_id):
    '''
    Get a dictionary of SNP data corresponding to the SNP identification.
    '''

    # initialize the dictionary
    snps_data_dict = {}

    # query
    sentence = f'''
                SELECT variant_id, ref, alt, sample_gt_list, sample_withmd_list
                    FROM vcf_snps
                    WHERE variant_id = '{snp_id}';
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

    # add row data to the dictionary
    for row in rows:
        snps_data_dict = {'variant_id': row[0], 'ref': row[1], 'alt': row[2], 'sample_gt_list': row[3], 'sample_withmd_list': row[4]}

    # return the dictionary
    return snps_data_dict

#-------------------------------------------------------------------------------
# query "get_snp_ids_list"
#-------------------------------------------------------------------------------

def get_snp_ids_list(conn):
    '''
    Get a list corresponding to all variant identifications.
    '''

    # initialize the list
    variant_id_list = []

    # query
    sentence = '''
               SELECT variant_id
                   FROM vcf_snps;
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

    # add the variant identification to the list
    for row in rows:
        variant_id_list.append(row[0])

    # return the list
    return variant_id_list

#-------------------------------------------------------------------------------
# query "get_snp_ids_wmd_list"
#-------------------------------------------------------------------------------

def get_snp_ids_wmd_list(conn):
    '''
    Get a list corresponding to the variant identifications with missing data.
    '''

    # initialize the list
    variant_id_list = []

    # query
    sentence = '''
               SELECT variant_id
                   FROM vcf_snps
                   WHERE length(sample_withmd_list) > 0;
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

    # add the variant identification to the list
    for row in rows:
        variant_id_list.append(row[0])

    # return the list
    return variant_id_list

#-------------------------------------------------------------------------------
# table "vcf_linkage_disequilibrium"
#-------------------------------------------------------------------------------

def drop_vcf_linkage_disequilibrium(conn):
    '''
    Drop the table "vcf_linkage_disequilibrium" (if it exists)
    '''

    sentence = '''
               DROP TABLE IF EXISTS vcf_linkage_disequilibrium;
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

#-------------------------------------------------------------------------------

def create_vcf_linkage_disequilibrium(conn):
    '''
    Create the table "vcf_linkage_disequilibrium".
    '''

    sentence = '''
               CREATE TABLE vcf_linkage_disequilibrium (
                   snp_id_1             TEXT NOT NULL,
                   snp_id_2             TEXT NOT NULL,
                   dhat                 REAL NOT NULL,
                   r2                   REAL NOT NULL,
                   sample_withmd_list_2 TEXT);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

#-------------------------------------------------------------------------------

def create_vcf_linkage_disequilibrium_index(conn):
    '''
    Create the unique index "vcf_linkage_disequilibrium_index" with the columns "snp_id_1" and "snp_id_2" on the table "vcf_linkage_disequilibrium"
    '''

    sentence = '''
               CREATE UNIQUE INDEX vcf_linkage_disequilibrium_index
                   ON vcf_linkage_disequilibrium (snp_id_1, snp_id_2);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

#-------------------------------------------------------------------------------

def insert_vcf_linkage_disequilibrium_row(conn, row_dict):
    '''
    Insert a row into table "vcf_linkage_disequilibrium"
    '''

    sentence = f'''
                INSERT INTO vcf_linkage_disequilibrium
                    (snp_id_1, snp_id_2, dhat, r2, sample_withmd_list_2)
                    VALUES ('{row_dict["snp_id_1"]}', '{row_dict["snp_id_2"]}', {row_dict["dhat"]}, {row_dict["r2"]}, '{row_dict["sample_withmd_list_2"]}')
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

#-------------------------------------------------------------------------------

def check_vcf_linkage_disequilibrium(conn):
    '''
    Check if table "vcf_linkage_disequilibrium" exists and if there are rows.
    '''

    # initialize the control variable
    control = 0

    # check if table "vcf_linkage_disequilibrium" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'vcf_linkage_disequilibrium'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "vcf_linkage_disequilibrium" exists
    if control == 1:

        sentence = '''
                   SELECT EXISTS
                       (SELECT 1
                           FROM vcf_linkage_disequilibrium
                           LIMIT 1);
                   '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise genlib.ProgramException(e, 'B002', sentence, conn)


        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the control variable
    return control

#-------------------------------------------------------------------------------

def get_vcf_linkage_disequilibrium_snp_id_1_list(conn):
    '''
    Get a list of variant identifications with linkage disequilibrium data.
    '''

    # initialize the list
    snp_id_1_list = []

    # query
    sentence = '''
               SELECT DISTINCT snp_id_1
                   FROM vcf_linkage_disequilibrium;
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

    # add row data to the dictionary
    for row in rows:
        snp_id_1_list.append(row[0])

    # return the list
    return snp_id_1_list

#-------------------------------------------------------------------------------

def get_vcf_linkage_disequilibrium_list(conn, snp_id_1):
    '''
    Get a list of linkage disequilibrium data corresponding to a variant.
    '''

    # initialize the list
    linkage_disequilibrium_list = []

    # query
    sentence = f'''
                SELECT snp_id_2, dhat, r2, sample_withmd_list_2
                    FROM vcf_linkage_disequilibrium
                    WHERE snp_id_1 = '{snp_id_1}';
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

    # add row data to the dictionary
    for row in rows:
        linkage_disequilibrium_list.append([row[0], row[1], row[2], row[3]])

    # return the list
    return linkage_disequilibrium_list

#-------------------------------------------------------------------------------

def get_vcf_linkage_disequilibrium_r2_measures(conn):
    '''
    Get global measures of r2 from linkage disequilibrium data.
    '''

    # create the SQL aggregate function "STDEV" in the database
    conn.create_aggregate("STDEV", 1, Stdev)

    # initialize data
    avg = 0
    stdev = 0

    # query
    sentence = '''
               SELECT AVG(r2), STDEV(r2)
                   FROM vcf_linkage_disequilibrium
                   where r2 >= 0;
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

    # get the row number
    for row in rows:
        avg = float(row[0])
        stdev = float(row[1])
        break

    # return the list
    return avg, stdev

#-------------------------------------------------------------------------------
# table "vcf_kinship"
#-------------------------------------------------------------------------------

def drop_vcf_kinship(conn):
    '''
    Drop the table "vcf_kinship" (if it exists)
    '''

    sentence = '''
               DROP TABLE IF EXISTS vcf_kinship;
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

#-------------------------------------------------------------------------------

def create_vcf_kinship(conn):
    '''
    Create the table "vcf_kinship".
    '''

    sentence = '''
               CREATE TABLE vcf_kinship (
                   individual_i INTEGER NOT NULL,
                   individual_j INTEGER NOT NULL,
                   rbeta        REAL    NOT NULL,
                   rw           REAL    NOT NULL,
                   ru           REAL    NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

#-------------------------------------------------------------------------------

def create_vcf_kinship_index(conn):
    '''
    Create the unique index "vcf_kinship_index" with the columns "individual_i" and "individual_j" on the table "vcf_kinship"
    '''

    sentence = '''
               CREATE UNIQUE INDEX vcf_kinship_index
                   ON vcf_kinship (individual_i, individual_j);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

#-------------------------------------------------------------------------------

def insert_vcf_kinship_row(conn, row_dict):
    '''
    Insert a row into table "vcf_kinship"
    '''

    sentence = f'''
                INSERT INTO vcf_kinship
                    (individual_i, individual_j, rbeta, rw, ru)
                    VALUES ({row_dict["individual_i"]}, {row_dict["individual_j"]}, {row_dict["rbeta"]}, {row_dict["rw"]}, {row_dict["ru"]})
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

#-------------------------------------------------------------------------------

def check_vcf_kinship(conn):
    '''
    Check if table "vcf_kinship" exists and if there are rows.
    '''

    # initialize the control variable
    control = 0

    # check if table "vcf_kinship" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'vcf_kinship'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "vcf_kinship" exists
    if control == 1:

        # select the row number
        sentence = '''
                   SELECT EXISTS
                       (SELECT 1
                           FROM vcf_kinship
                           LIMIT 1);
                   '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise genlib.ProgramException(e, 'B002', sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the control variable
    return control

#-------------------------------------------------------------------------------

def get_vcf_kinship_dict(conn):
    '''
    Get a dictionary corresponding to kinship data.
    '''

    # initialize the dictionary
    kinship_dict = genlib.NestedDefaultDict()

    # query
    sentence = '''
               SELECT individual_i, individual_j, rbeta, rw, ru
                   FROM vcf_kinship;
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise genlib.ProgramException(e, 'B002', sentence, conn)

    # add row data to the dictionary
    for row in rows:
        kinship_dict[row[0]][row[1]] = {'rbeta': row[2], 'rw': row[3], 'ru': row[4]}

    return kinship_dict

#-------------------------------------------------------------------------------
# General classes
#-------------------------------------------------------------------------------

class Stdev:
    '''
    This class defines the calculation of standard deviation
    (SQLite does not have a function for standard deviation).
    '''

    #---------------

    def __init__(self):

        self.M = 0.0
        self.S = 0.0
        self.k = 1

    #---------------

    def step(self, value):

        if value is None:
            return

        tM = self.M
        self.M += (value - tM) / self.k
        self.S += (value - tM) * (value - self.M)
        self.k += 1

    #---------------

    def finalize(self):

        if self.k < 3:
            return None

        return math.sqrt(self.S / (self.k-2))

    #---------------

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print(f'This source contains functions for the maintenance of the SQLite databases used in {genlib.get_app_long_name()}.')
    sys.exit(0)

#-------------------------------------------------------------------------------
