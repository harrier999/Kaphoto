# Before Run
You Need to install `Docker` first

# With Docker
`docker-compose build`
`docker-compose up`

## when you delete container 
`docker-compose down`

# run without docker
## before run
pip3 install -r requirements_all.txt
## Frontend
streamlit run frontend/frontend.py --docker False

## backend
python SRGAN/main.py