import ibm_boto3
from ibm_botocore.client import Config, ClientError
import uuid
from flask import current_app


def get_uuid():
    return str(uuid.uuid4().hex)


def multi_part_upload(file_path):
    COS_ENDPOINT = current_app.config['COS_ENDPOINT']
    COS_API_KEY_ID = current_app.config['COS_API_KEY_ID']
    COS_INSTANCE_CRN = current_app.config['COS_INSTANCE_CRN']
    COS_BUCKET_NAME = current_app.config['COS_BUCKET_NAME']
    # Create resource
    cos = ibm_boto3.resource("s3",
                             ibm_api_key_id=COS_API_KEY_ID,
                             ibm_service_instance_id=COS_INSTANCE_CRN,
                             config=Config(signature_version="oauth"),
                             endpoint_url=COS_ENDPOINT
                             )
    item_name = get_uuid() + '.' + get_extension(file_path)
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(
            item_name, COS_BUCKET_NAME))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        with open(file_path, "rb") as file_data:
            cos.Object(COS_BUCKET_NAME, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
        return item_name  # send object name
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
        return 'none'  # no file
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))
        return 'none'  # no file


def get_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1]


def get_signed_url(receipt):

    bucket_name = current_app.config['COS_BUCKET_NAME']
    key_name = receipt
    http_method = 'get_object'
    expiration = 60  # time in seconds, default:600

    access_key = current_app.config['COS_HMAC_ACCESS_KEY']
    secret_key = current_app.config['COS_HMAC_SECRET_KEY']
    # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
    cos_service_endpoint = current_app.config['COS_ENDPOINT']

    cos = ibm_boto3.client("s3",
                           aws_access_key_id=access_key,
                           aws_secret_access_key=secret_key,
                           endpoint_url=cos_service_endpoint
                           )

    signedUrl = cos.generate_presigned_url(http_method, Params={
        'Bucket': bucket_name, 'Key': key_name}, ExpiresIn=expiration)
    return signedUrl
