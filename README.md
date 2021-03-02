# jeockovanibezpecne.cz

Source code for [jeockovanibezpecne.cz](https://jeockovanibezpecne.cz).

## Development

```bash
pyenv global 3.9.0          # we need at least python 3.7, get python your way use pyenv or something else
make install-dev            # setup all dependencies
source venv/bin/activate    # activate virtual environment
flask init-db               # creates sqlite db app.db
flask update                # downloads data from UZIS and SUKL
flask run                   # run the app in development mode
```

It uses environment variables prepared in [.env](./blob/main/.env). The server runs by default at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Heroku Setup

```bash
heroku git:remote -a jeockovanibezpecne
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set APP_SETTINGS=config.ProductionConfig
heroku config:set FLASK_APP=jsouvakcinybezpecne
heroku buildpacks:add --index 1 heroku/nodejs
heroku buildpacks:add --index 2 heroku/python
heroku domains:add jeockovanibezpecne.cz
heroku domains:wait 'jeockovanibezpecne.cz'
```
