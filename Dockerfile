FROM ulaskaraoz/kb_debmicrotrait2:latest

RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rjson/rjson_0.2.20.tar.gz', repos = NULL, type='source')"
RUN R -e "install.packages(c('GetoptLong', 'shape'), repos = 'https://cloud.r-project.org')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/circlize/circlize_0.4.15.tar.gz', repos = NULL, type='source')"
RUN R -e "BiocManager::install('ComplexHeatmap')"

RUN curl --location https://kbmicrotrait.s3.us-west-1.amazonaws.com/microtrait_1.0.0.tar.gz > /tmp/microtrait.tar.gz
RUN R -e "install.packages('/tmp/microtrait.tar.gz', repos = NULL, type='source')"
RUN R -e "microtrait::prep.hmmmodels()"
RUN pip install pypdf

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]

