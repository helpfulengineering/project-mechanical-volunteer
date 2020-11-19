FROM python:3.6-buster

ENV REDIS_SENTINEL=redis-sentinel
ENV REDIS_MASTER=mymaster

# install git and various python library dependencies with alpine tools
RUN set -x && \
    apt-get update && \
    apt-get install python-dev build-essential libjpeg-dev libssl-dev libffi-dev -y && \
    apt-get install dbus libdbus-1-dev libdbus-glib-1-dev libldap2-dev libsasl2-dev -y

# install python dependencies with pip
# install pybossa from git
# add unprivileged user for running the service
ENV LIBRARY_PATH=/lib:/usr/lib
RUN set -x && \
    git clone --recursive https://github.com/Scifabric/pybossa /opt/pybossa && \
    cd /opt/pybossa && \
    pip install -U pip setuptools && \
    pip install -r /opt/pybossa/requirements.txt && \
    rm -rf /opt/pybossa/.git/ && \
    addgroup pybossa  && \
    adduser --disabled-password --gecos "" --home /opt/pybossa --ingroup pybossa pybossa && \
    passwd -u pybossa

# variables in these files are modified with sed from /entrypoint.sh
ADD alembic.ini /opt/pybossa/
ADD settings_local.py /opt/pybossa/

COPY ./plugins/healthsites-importer/plugin /opt/pybossa/pybossa/plugins/healthsites_importer
COPY ./plugins/healthsites-importer/themes /opt/pybossa/pybossa/themes
#COPY ./plugins/healthsites-importer/forms/healthsites_import_form.py /opt/pybossa/pybossa/forms

# TODO: we shouldn't need write permissions on the whole folder
#   Known files written during runtime:
#     - /opt/pybossa/pybossa/themes/default/static/.webassets-cache
#     - /opt/pybossa/alembic.ini and /opt/pybossa/settings_local.py (from entrypoint.sh)

# run with unprivileged user
RUN chown -R pybossa:pybossa /opt/pybossa
COPY --chown=pybossa entrypoint.sh /
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# run with unprivileged user
WORKDIR /opt/pybossa
USER pybossa
EXPOSE 8080

# Background worker is also necessary and should be run from another copy of this container
#   python app_context_rqworker.py scheduled_jobs super high medium low email maintenance
CMD ["python", "run.py"] 