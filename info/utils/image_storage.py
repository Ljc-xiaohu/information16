from qiniu import Auth, put_file, etag, put_data
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = '2NXiog9dYLwssgPhb74CuziGbetrbAWfPNVqYs_R'
secret_key = '3IjLRJGMuVriaTz19avDZ4pbi3jZc0JHu-IC50xY'


def image_storage(image_data):
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'info016'

    # 上传到七牛后保存的文件名
    # 如果不传名称,由七牛云维护图片名字
    # key = 'my-python-logo.png'
    key = None

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    # localfile = './11.gif'
    # ret, info = put_file(token, key, localfile)
    ret, info = put_data(token, key, image_data)

    # print(info)
    # print(ret)

    # 返回上传的状态
    if info.status_code == 200:
        return ret.get("key")
    else:
        return ""


# 测试
if __name__ == '__main__':
    # 方式一:
    # f = open("./11.gif","rb")
    # image_storage(f.read())
    # f.close()

    # 方式二:
    with open("./11.gif", "rb") as f:
        image_name = image_storage(f.read())
        print(image_name)
