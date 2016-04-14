# -*- coding: utf-8 -*-

from formats_common import *

enable = True
format = 'MtuxMdic'
description = 'SQLite(MDic m2, Sib sdb)'
extentions = ['.m2', '.sdb']
readOptions = []
writeOptions = ['keyAlters']

infoKeys = [
    'dbname',
    'author',
    'version',
    'direction',
    'origLang',
    'destLang',
    'license',
    'category',
    'description',
]

def read(glos, filename):
    from sqlite3 import connect

    ## ???????? name OR dbname ????????????????????
    con = connect(filename)
    cur = con.cursor()
    for key in infoKeys:
        try:
            cur.execute('select %s from dbinfo'%key)
        except:
            pass
        else:
            value = cur.fetchone()[0].encode('utf8')
            if value!='':
                glos.setInfo(key, value)
    cur.execute('select * from word')
    for x in cur.fetchall():
        try:
            w = x[1].encode('utf8')
            m = x[2].encode('utf8')
        except:
            log.error('error while encoding word %s'%x[0])
        else:
            glos.addEntry(w, m)
    cur.close()
    con.close()
    return True

def read_2(glos, filename):
    import pyglossary.alchemy as alchemy
    return alchemy.readSqlite(glos, filename)


def write_2(glos, filename):
    import pyglossary.alchemy as alchemy
    alchemy.writeSqlite(glos, filename)

def write_3(glos, filename):
    import pyglossary.exir as exir
    exir.writeSqlite_ex(glos, filename)
    return True

def write(glos, filename, **options):
    from sqlite3 import connect
    if os.path.exists(filename):
        os.remove(filename)
    con = connect(filename)
    cur = con.cursor()
    sqlLines = glos.getSqlLines(
        infoKeys=infoKeys,
        newline='<BR>',
        transaction=False,
    )
    if options and 'keyAlters' in options:
        addSqlVariantsTable(sqlLines, options['keyAlters'])
    n = len(sqlLines)
    ui = glos.ui
    if ui:
        ui.progressStart()
        k = 1000
        for i in xrange(n):
            try:
                con.execute(sqlLines[i])
            except:
                log.exception('error executing sqlite query:')
                log.error('Error while executing: '+sqlLines[i])
                continue
            if i%k==0:
                rat = float(i)/n
                ui.progress(rat)
        ui.progressEnd()
    else:
        for i in xrange(n):
            try:
                cur.execute(sqlLines[i])
            except:
                log.exception('error executing sqlite query:')
                log.error('Error while executing: '+sqlLines[i])
                continue
    if options and 'keyAlters' in options:
        #set correct base_w_id
        cur.execute('SELECT v, base_word FROM variants')
        i = 0
        for x in cur.fetchall():
            try:
                variant = x[0]
                base = x[1]
                variant = variant.replace('\'', '\'\'')
                base = base.replace('\'', '\'\'')
            except:
                log.error('error while encoding variant %s' % x[0])
            else:
                cur.execute('SELECT id FROM word WHERE w=\'%s\';' % base)
                base_w_id = cur.fetchone()[0]
                cur.execute('UPDATE variants SET base_w_id=%d WHERE v=\'%s\';' % (base_w_id, variant))

    cur.close()
    con.commit()
    con.close()
    return True

def addSqlVariantsTable(lines, keyAlters):
    lines.append('CREATE TABLE variants (\'id\' INTEGER PRIMARY KEY NOT NULL, \'v\' TEXT, \'base_w_id\' INTEGER, \'base_word\' TEXT);')
    for i, pair in enumerate(keyAlters):
        variant = pair[0]
        base = pair[1]
        variant = variant.replace('\'', '\'\'')
        base = base.replace('\'', '\'\'')
        lines.append('INSERT INTO variants VALUES(%d, \'%s\', %d, \'%s\');' % (i + 1, variant, 0, base))
    lines.append('CREATE INDEX ix_variants_v ON variants(v COLLATE NOCASE);')