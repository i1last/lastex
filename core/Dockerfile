# --- УСТАНОВКА ОБРАЗА ---
# FROM texlive/texlive:latest-small
FROM registry.gitlab.com/islandoftex/images/texlive:TL2025-2025-11-02-small
 
ENV TERM=dumb
 
# --- УСТАНОВКА ПАКЕТОВ ---
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3 python3-pygments
RUN rm -rf /var/lib/apt/lists/*

RUN tlmgr update --self && tlmgr install texfot latexmk
RUN tlmgr update --self && tlmgr install \
    collection-latexrecommended \
    collection-luatex \
    collection-langcyrillic \
    collection-context \ 
    collection-bibtexextra
RUN tlmgr update --self && tlmgr install \
    biber \
    biblatex \
    biblatex-gost \
    csquotes \
    tabularray \
    xurl \
    zref \
    ninecolors \
    cleveref \
    enumitem \
    makecell \
    was \
    multirow \
    tocloft \
    titlesec \
    minted \
    appendix \
    enotez \
    translations
RUN tlmgr update --self && tlmgr install \
    circuitikz \
    pgf \
    pgfplots \
    wrapfig
RUN apt-get update && apt-get install -y \
    python3 \
    python3-numpy \
    python3-matplotlib \
    python3-scipy \
    && rm -rf /var/lib/apt/lists/*
    
RUN mktexlsr && tlmgr path add && fmtutil-sys --all

# --- УСТАНОВКА ЛОКАЛЬНЫХ ШРИФТОВ ---
RUN mkdir -p /usr/local/share/fonts/truetype/times-new-roman
COPY core/fonts/times.ttf /usr/local/share/fonts/truetype/times-new-roman/
COPY core/fonts/timesbd.ttf /usr/local/share/fonts/truetype/times-new-roman/
COPY core/fonts/timesi.ttf /usr/local/share/fonts/truetype/times-new-roman/
COPY core/fonts/timesbi.ttf /usr/local/share/fonts/truetype/times-new-roman/
RUN mkdir -p /usr/local/share/fonts/truetype/jb-mono
COPY core/fonts/JetBrainsMono-Regular.ttf /usr/local/share/fonts/truetype/jb-mono/
COPY core/fonts/JetBrainsMono-Bold.ttf /usr/local/share/fonts/truetype/jb-mono/
COPY core/fonts/JetBrainsMono-Italic.ttf /usr/local/share/fonts/truetype/jb-mono/
COPY core/fonts/JetBrainsMono-BoldItalic.ttf /usr/local/share/fonts/truetype/jb-mono/

# --- КОПИРОВАНИЕ КОНФИГА MATPLOTLIB ---
COPY core/matplotlibrc /etc/matplotlibrc

# --- ПРЕДВАРИТЕЛЬНАЯ ГЕНЕРАЦИЯ БАЗ ДАННЫХ ---
RUN fc-cache -f -v
RUN mkdir -p /root/.texlive2024/texmf-var/luatex-cache
RUN luaotfload-tool --update --force
RUN mtxrun --generate
RUN fmtutil-sys --byfmt lualatex
RUN fmtutil-sys --all


WORKDIR /workdir
