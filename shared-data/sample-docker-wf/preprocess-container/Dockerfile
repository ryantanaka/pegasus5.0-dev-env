FROM python:3.7-alpine

RUN apk update \
        && apk add --no-cache git perl curl wget \
        && cd /tmp \
        && git clone https://github.com/jasonm23/cowsay.git \
        && cd cowsay ; ./install.sh /usr/local \
        && rm -rf /var/cache/apk/* /var/tmp/* /tmp/* \
        && apk del git

RUN pip install emoji

RUN printf "#!/bin/ash\n(cat \$1 | cowsay && echo 'This is your processed ML data!') | cat > \$2\n" >> /usr/local/bin/preprocess.sh \
    && chmod a+x /usr/local/bin/preprocess.sh 


