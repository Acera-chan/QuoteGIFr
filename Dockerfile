FROM python:3.7-slim-buster

#RUN sed -i "/^# deb .*multiverse/ s/^# //" /etc/apt/sources.list

# RUN echo "deb http://httpredir.debian.org/debian jessie main contrib" > /etc/apt/sources.list \
#     && echo "deb http://security.debian.org/ jessie/updates main contrib" >> /etc/apt/sources.list \
#     && echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections \
#     && apt-get update \
#     && apt-get install -y lsb-base \
#     && apt-get install -y x11-common xfonts-encodings \
#     && apt-get install -y xfonts-utils \
#     && apt-get install -y ttf-mscorefonts-installer \    
#     && apt-get clean \
#     && apt-get autoremove -y \
#     && rm -rf /var/lib/apt/lists/*


# install dependancies
RUN apt-get -y update \
    && apt-get install -y ffmpeg imagemagick \
    && apt-get install -y wget \
    && apt-get install -y cabextract xfonts-utils

RUN rm -rf /var/lib/apt/lists/*

RUN wget http://ftp.de.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.6_all.deb
RUN dpkg -i ttf-mscorefonts-installer_3.6_all.deb


#RUN wget --content-disposition -P /usr/share/fonts/truetype/robotomono \
#        https://github.com/google/fonts/blob/master/apache/robotomono/static/RobotoMono-Medium.ttf?raw=true

# set working directory
WORKDIR "G:\Users\Tempest3\Documents\USCU\Fall 2019\Software Engineering\QuoteGIFr\github_repo"

# fix ImageMagick policies
COPY policy.xml /etc/ImageMagick-6/policy.xml

# copy requirements file
COPY QuoteGIFr/codebase/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# copy all files
COPY QuoteGIFr/codebase .

ENTRYPOINT ["python3"]
CMD ["app.py"]