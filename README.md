# CreativeGamesBot

py -m venv env
.\env\Scripts\activate
deactivate
python.exe -m pip install --upgrade pip
pip3 install -r requirements.txt
pip3 install -U aiogram
pip3 install telebot
python3 -m pip install pyTelegramBotAPI six
pip3 install pyTelegramBotAPI six
pip3 install pipenv

pip3 install pyTelegramBotAPI

**DevOps CI/CD**
https://world-of-crypto-curreny.herokuapp.com/
https://dashboard.heroku.com/apps/world-of-crypto-curreny
heroku login
heroku git:clone -a creative-trade-in
cd TradeBotHeroku
git add .
git commit -am "make it better"
git push heroku master

git commit -am "fix issue #1"
git push heroku master
git checkout -b main
git branch -D master
git push heroku main

**Monitoring**
heroku run bash -a creative-trade-in
#https://dashboard.heroku.com/apps/world-of-crypto-currency/logs
heroku logs --tail 
heroku status
python ./bot1.py
heroku maintenance:on | heroku ps:scale web=0 | heroku restart
heroku maintenance:off