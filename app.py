from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
# import vk_api
# from vk_api import VkUpload
# import os


def send_mail(email: str, text: list):
    login = 'VictoRailways@yandex.ru'
    password = 'iwzkbnevhgmjxjja'
    text_mail = ''
    print(text, type(text))
    for i in text:
        print(i, type(i))
        text_mail+=i+'\n'
    msg = MIMEText(f'Добрый день, Ваша заявка на участие в конкурсе принята в обработку. \n\nДанные которые мы от Вас получили:\n {text_mail}\n\nВ случае некорректого получения нами данных, свяжитесь с нами в группе в ВКонтакте. ', 'plain','utf-8' )
    msg['Subject'] = Header('Конкурс  видеоинтервью "Железные дороги победы"')
    msg['From'] = login
    msg['To'] = email

    s = smtplib.SMTP('smtp.yandex.ru', 587, timeout=10)
    try:
        s.starttls()
        s.login(login,password)
        s.sendmail(msg['From'],email, msg.as_string())
    except:
        print('Error send mail')
    finally:
        s.quit()


year_now = 2024

application = Flask(__name__)
application.secret_key = 'KvantoriumZHDPYal4'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)
# session = vk_api.VkApi(login='+79826550610', password='VictoryRails2023', app_id=2685278)
# session.auth(token_only=True)
# vk = session.get_api()


url = 'https://api.vk.com/method/wall.get'
token = 'vk1.a.PB50JZDEvtlvwpCkLFi_fZhT0VMUpnZvBxtL6duVq3tK0WqeTr45UGcJzOlhe9fNiR5-TLPV2fSke9SbCX3epOqtTPsTBb90FLKszoxeFOjxgONi63KeqfDl-839s0gScAWFNEUFLm66Vb5UDjNOvv4lF_qReTci-3_mpb67HcLcHje42sT9FkOTbiyXsBn3DGZiBb7WCZlsVoCGtKNaRw'
group_id = -216704492
posts = 2


def getActiveBtn(active, aside):
    # print(str(active))
    # print(aside,end="\n\n end \n")

    return "but_sort_active" if str(active) in aside else ""


@application.context_processor
def context_processor():
    return dict(getActiveBtn=getActiveBtn)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, nullable=True)
    video_url = db.Column(db.String, nullable=True)
    video_hash = db.Column(db.String, nullable=True)

    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String, nullable=False)
    locality = db.Column(db.String, nullable=False)
    e_institution = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    participants1 = db.Column(db.String, nullable=False)
    partdr1 = db.Column(db.String, nullable=False)
    participants2 = db.Column(db.String)
    partdr2 = db.Column(db.String)
    participants3 = db.Column(db.String)
    partdr3 = db.Column(db.String)
    participants4 = db.Column(db.String)
    partdr4 = db.Column(db.String)
    participants5 = db.Column(db.String)
    partdr5 = db.Column(db.String)
    curator = db.Column(db.String, nullable=False)
    curator_phone = db.Column(db.String, nullable=False)
    curator_email = db.Column(db.String, nullable=False)
    where_find = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    moder = db.Column(db.Integer, default =0)


application.app_context().push()
db.create_all()


@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@application.route('/archive', methods=['GET', 'POST'])
def archive():
    year = request.args.get('y')
    search = request.args.get('s')
    posts = Posts.query.filter(Posts.video_url != None)
    all_posts = posts
    if year != None and search == None:
        print(1)

        posts = []
        for post in all_posts:
            if post.year == int(year):
                posts.append(post)
            print(posts)
    if search != None and year == None:
        print(2)
        posts = []
        print(all_posts)
        for post in all_posts:

            if (search.lower() in post.title.lower()) or (search.lower() in post.description.lower()) or (
                    search.lower() in post.locality.lower()) or (search.lower() in post.e_institution.lower()) or (
                    search.lower() in post.region.lower()) or (search.lower() in post.participants1.lower()) :
                posts.append(post)

    if search != None and year != None:
        print(3)
        posts = []
        for post in all_posts:
            if ((search.lower() in post.title.lower()) or (search.lower() in post.description.lower()) or (
                    search.lower() in post.locality.lower()) or (search.lower() in post.e_institution.lower()) or (
                        search.lower() in post.region.lower()) or (
                        search.lower() in post.participants.lower())) and post.year == int(year):
                posts.append(post)
    return render_template('archive.html', posts=posts)


@application.route('/file', methods=['GET', 'POST'])
def file_drop():
    if request.method == 'POST':
        # добавить трай эксепт и флеш уведомление для невозможности отправки пустоты
        try:
            print(request.form)
            video_file = request.form.get('video_file')
            print(video_file)
            title = request.form.get('title')
            description = request.form.get('description')
            category = int(request.form.get('category'))
            region = request.form.get('region')
            locality = request.form.get('city')
            e_institution = request.form.get('e_institution')
            address = request.form.get('address')
            participants1 = request.form.get('participants1')
            partdr1 = request.form.get('date_participants1')
            participants2 = request.form.get('participants2')
            # print(type(participants1))
            # print(type(partdr1))
            partdr2 = request.form.get('date_participants2')
            participants3 = request.form.get('participants3')
            partdr3 = request.form.get('date_participants3')
            participants4 = request.form.get('participants4')
            partdr4 = request.form.get('date_participants4')
            participants5 = request.form.get('participants5')
            partdr5 = request.form.get('date_participants5')
            curator = request.form.get('curator')
            curator_phone = request.form.get('phone')
            curator_email = request.form.get('email')
            where_find = request.form.get('where_find')
            new_post = Posts(title=title,
                             description=description,
                             category=category,
                             region=region,
                             locality=locality,
                             e_institution=e_institution,
                             address=address,
                             participants1=participants1,
                             partdr1 = partdr1,
                             participants2=participants2,
                             partdr2 = partdr2,
                             participants3=participants3,
                             partdr3 = partdr3,
                             participants4=participants4,
                             partdr4 = partdr4,
                             participants5=participants5,
                             partdr5 = partdr5,
                             curator=curator,
                             curator_phone=curator_phone,
                             curator_email=curator_email,
                             where_find=where_find,
                             year=year_now)
            db.session.add(new_post)
            db.session.commit()
            # with open(f'{new_post.id}.mp4', 'wb') as new_file:
            #     new_file.write(video_file.read())
            # up = VkUpload(vk)
            # video = up.video(f'{new_post.id}.mp4',
            #                  name=f'{year_now} | {title}',
            #                  description=f'{participants}\n\n{description}',
            #                  group_id=219650731)
            # os.remove(f'{new_post.id}.mp4')
            # new_post.video_id = video.get('video_id')
            # db.session.commit()
            group_id = int(video_file[video_file.find('-'):video_file.find('_')])

            response = requests.get(
                url=url,
                params={
                    'access_token': token,
                    'owner_id': group_id,
                    'v': '5.199',
                }
            )
            # new_post.video_id = response.json()['response']['items'][0]['attachments'][0]["video"]["id"]
            # new_post.video_url = f'https://vk.com/video_ext.php?oid={group_id}&id={new_post.video_id}&hd=3'
            new_post.video_url =  video_file
            db.session.commit()
            text_mail=[
                 f'Название работы: {title}',
                 f'Ссылка на видео интервью: {video_file}',
                 f'Описание: {description}',
                 f"Категория (если Ваша категория 10-15,то должен быть 0,иначе 1): {category}",
                 f'Регион: {region}',
                 f'Населенный пункт: {locality}',
                 f'Образовательное учреждение: {e_institution}',
                 f'Адрес ОУ: {address}',
                 f'ФИО 1ого учасника: {participants1}',
                 f'Дата рождения 1ого участника: {partdr1}',
                 f'ФИО 2ого учасника: {participants2}',
                 f'Дата рождения 2ого участника: {partdr2}',
                 f'ФИО 3ого учасника: {participants3}',
                 f'Дата рождения 3ого участника: {partdr3}',
                 f'ФИО 4ого учасника (актуально только для категории 10-15 лет): {participants4}',
                 f'Дата рождения 4ого участника: {partdr4}',
                 f'ФИО 5ого учасника(актуально только для категории 10-15 лет): {participants5}',
                 f'Дата рождения 5ого участника: {partdr5}',
                 f'ФИО куратора: {curator}',
                 f'Телефон кулатора: {curator_phone}',
                 f'Email куратора: {curator_email}',
                 f'Откуда о нас узнали: {where_find}'

            ]
            send_mail(curator_email, text_mail)
        except:
            # flash()
            return render_template('file.html')
        return redirect(url_for('index'))
    return render_template('file.html')


@application.route('/file_old/<int:year_to_drop>', methods=['GET', 'POST'])
def file_drop_old(year_to_drop):
    if request.method == 'POST':
        video_file = request.files['video_file']
        title = request.form.get('title')
        description = request.form.get('description')
        category = int(request.form.get('category'))
        region = request.form.get('region')
        locality = request.form.get('city')
        e_institution = request.form.get('e_institution')
        address = request.form.get('address')
        participants = request.form.get('participants')
        curator = request.form.get('curator')
        curator_phone = request.form.get('phone')
        curator_email = request.form.get('email')
        where_find = request.form.get('where_find')
        new_post = Posts(title=title,
                         description=description,
                         category=category,
                         region=region,
                         locality=locality,
                         e_institution=e_institution,
                         address=address,
                         participants=participants,
                         curator=curator,
                         curator_phone=curator_phone,
                         curator_email=curator_email,
                         where_find=where_find,
                         year=year_to_drop)
        db.session.add(new_post)
        db.session.commit()
        # with open(f'{new_post.id}.mp4', 'wb') as new_file:
        #     new_file.write(video_file.read())
        # up = VkUpload(vk)
        # video = up.video(f'{new_post.id}.mp4',
        #                  name=f'{year_to_drop} | {title}',
        #                  description=f'{participants}\n\n{description}',
        #                  group_id=219650731)
        # os.remove(f'{new_post.id}.mp4')гей
        # new_post.video_id = video.get('video_id')
        # db.session.commit()
        return redirect(url_for('index'))
    return render_template('file.html')


# @application.route('/r', methods=['GET'])
# def refresh_hash():
#     without_hash = Posts.query.filter(Posts.video_hash == None)
#     print(without_hash)
#     for vid in without_hash:
#         print(vid.id)
#     for item in vk.video.get(owner_id=-219650731).get('items'):
#         for vid in without_hash:
#             print(item.get('id'), vid.video_id)
#             if item.get('id') == vid.video_id:
#                 vid.video_hash = item.get('player')[62:78]
#                 print(vid.video_hash)
#                 vid.video_url = f'https://vk.com/video_ext.php?oid=-219650731&id={vid.video_id}&hash={vid.video_hash}&hd=3'
#     db.session.commit()
#     return redirect(url_for('index'))

@application.route('/test_form')
def testform():
    return render_template('testfile.html')

@application.route('/expert')
def ocenka():
    return render_template('ocenka.html')




if __name__ == '__main__':
    application.run('0.0.0.0', debug=True)
