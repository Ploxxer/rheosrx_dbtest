import psycopg2
import requests
from simplejson import loads
import csv
import urllib
import boto3
import datetime

print('start')
s3 = boto3.client('s3')
print('s3 client created')
conn = psycopg2.connect(dbname='postgres', user='ploxxer', host='postgrestest.ce7lvgdrslb3.us-east-1.rds.amazonaws.com',
                        password='siren55555')
cur = conn.cursor()

print('connection created')
def dbrecord():
    with open('/tmp/temp.csv', 'r') as f:
        with open('/tmp/modified_file.csv', 'w') as w:
            f.next()
            for line in f:
                w.write(line)
    print('creating record')
    with open('/tmp/modified_file.csv', 'r') as r:

        cur.copy_from(r, 'donor_id', sep = ',' , columns = ('donorid', 'createdby', 'datarecordname', 'relatedrecord3', 'externalid', 'datecreated', 'gender', 'recordid', 'vendor', 'datatype', 'record_id'))
	conn.commit()


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    obj = s3.get_object(Bucket=bucket, Key=key)

    auth = ('sapio.api@rheosrx.com', 'rheos123!')
    headers = {'guid': 'b9d2001e-137b-4c1c-9778-9ce2bdbe8ad3'}

    lines = obj['Body'].read().decode('utf-8').splitlines(True)
    rdr = csv.reader(lines)

    inner_dict = []
    data = []

    s3.download_file(bucket, key, '/tmp/temp.csv')
    with open('/tmp/test_file_2_modified.csv', 'w') as result:
        wtr = csv.writer(result)
        for r in rdr:
            wtr.writerow((r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]))

    with open('/tmp/test_file_2_modified.csv', 'r') as data_file:
        reader = csv.DictReader(data_file, delimiter=',')
        for row in reader:
            inner_dict = {'fields': row, 'datatype': 'Donor', 'record_id': None}

    data.append(inner_dict)

    get_url = 'https://node-25.exemplareln.com:8443/velox_webservice/api/datarecord?datatype=Donor'
    resp3 = requests.get(get_url, auth=auth, headers=headers)
    counter = 0
    dupe_list = []

    for i in range(0, len(loads(resp3.content))):
        if counter != len(loads(resp3.content)):
            dupe_list.append(loads(resp3.content)[counter]['fields'].get('ExternalId'))
            counter += 1

    print(data)

    if data[0]['fields'].get('ExternalId') not in dupe_list:
        dbrecord()
        print('got through creating record')

        post_url = 'https://node-25.exemplareln.com:8443/velox_webservice/api/datarecord'

        resp = requests.post(post_url, auth=auth, headers=headers, json=data)

        put_url = 'https://node-25.exemplareln.com:8443/velox_webservice/api/datarecord/child/add?datatype=Directory&record_id=2344'

        data2 = [[{
            "datatype": "Donor",
            "record_id": str(loads(resp.content)[0].get("record_id"))
        }]]

        requests.put(put_url, auth=auth, headers=headers, json=data2)

        get_url = 'https://node-25.exemplareln.com:8443/velox_webservice/api/datarecord?datatype=Donor&field=ExternalId&values=' + str(
            data[0]['fields'].get('ExternalId'))

        resp2 = requests.get(get_url, auth=auth, headers=headers)

        content = loads(resp2.content)
        donorid = (content[0]['fields']['DonorId'])
        datarecordname = str(content[0]['fields']['DataRecordName'])
        datecreated = content[0]['fields']['DateCreated']
        recordid = str(content[0]['fields']['RecordId'])
        record_id = str(content[0]['record_id'])
        createdby = str(content[0]['fields']['CreatedBy'])
        gender = str(content[0]['fields']['Gender'])
        vendor = str(content[0]['fields']['Vendor'])

        externalid = str(data[0]['fields'].get('ExternalId'))

        print(donorid)
        print(createdby)
        print(datarecordname)
        print(datecreated)
        print(gender)
        print(recordid)
        print(vendor)
        print(record_id)

        print(externalid)

        date = str(datetime.datetime.fromtimestamp(datecreated / 1e3))

        sqlstr = "UPDATE donor_id SET donorid =  '" + donorid + "', CreatedBy ='" + createdby + "', datarecordname ='" + datarecordname + "', datecreated = '" + date + "', Gender = '" + gender + "', recordid = " + recordid + ", Vendor ='" + vendor + "', record_id = " + record_id + " WHERE externalid = '" + externalid + "'"

        print(sqlstr)
        cur.execute(sqlstr)

        conn.commit()
	conn.close()
        print('donor created')

    else:
        print('dupe found')

    print('reached end')
    return
