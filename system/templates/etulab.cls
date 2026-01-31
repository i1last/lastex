\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{etulab}[2025/01/31 v1.0 ETU Lab Report Class]

\LoadClass[a4paper,14pt,russian]{extarticle}

% --- Настройка шрифтов
\RequirePackage{fontspec}
\RequirePackage{polyglossia}

\setmainlanguage{russian}
\setotherlanguage{english}

% \setmainfont{TeX Gyre Termes}  % Свободный аналог Times New Roman, включенный в TeX Live
\setmainfont{Times New Roman}[
    Path            = /usr/local/share/fonts/truetype/times-new-roman/,  % Путь внутри контейнера
    Extension       = .ttf,
    UprightFont     = times,
    BoldFont        = timesbd,
    ItalicFont      = timesi,
    BoldItalicFont  = timesbi
]

\setmonofont{JetBrains Mono}[
    Path            = /usr/local/share/fonts/truetype/jb-mono/,  % Путь внутри контейнера
    Extension       = .ttf,
    UprightFont     = JetBrainsMono-Regular,
    BoldFont        = JetBrainsMono-Bold,
    ItalicFont      = JetBrainsMono-Italic,
    BoldItalicFont  = JetBrainsMono-BoldItalic
]


% --- Импортирование стилей
% Определения
\RequirePackage{etulab/defs/cyrillic.def}            % Определения для корректной работы кириллицы
\RequirePackage{etulab/defs/appendixAsbuk.def}       % Определение счётчика приложений в виде русских букв

% Пакеты-зависимости
\RequirePackage{etulab/packages.sty}

% Настройки оформления
\RequirePackage{etulab/layouts/appendixes.sty}       % Настройка приложений
\RequirePackage{etulab/layouts/code.sty}             % Настройка листингов
\RequirePackage{etulab/layouts/figures.sty}          % Настройка рисунков
\RequirePackage{etulab/layouts/refs.sty}             % Настройка ссылок
\RequirePackage{etulab/layouts/tableOfContents.sty}  % Настройка Содержания
\RequirePackage{etulab/layouts/tables.sty}           % Настройка таблиц
\RequirePackage{etulab/layouts/typography.sty}       % Настройка типографики

% Определение пользовательских команд
\RequirePackage{etulab/commands.sty}


% --- Интерфейс данных
\newcommand{\Department}[1]{\def\@Department{#1}}
\newcommand{\WorkType}[1]{\def\@WorkType{#1}}
\newcommand{\Discipline}[1]{\def\@Discipline{#1}}
\newcommand{\WorkTitle}[1]{\def\@WorkTitle{#1}}
\newcommand{\Group}[1]{\def\@Group{#1}}
\newcommand{\Variant}[1]{\def\@Variant{#1}}
\newcommand{\StudentName}[1]{\def\@StudentName{#1}}
\newcommand{\TeacherName}[1]{\def\@TeacherName{#1}}
\newcommand{\Year}[1]{\def\@Year{#1}}

% Значения по умолчанию
\def\@Department{КАФЕДРА}
\def\@WorkType{ТИП_РАБОТЫ}
\def\@Discipline{ДИСЦИПЛИНА}
\def\@WorkTitle{ТЕМА РАБОТЫ}
\def\@Group{0000}
\def\@Variant{0}
\def\@StudentName{ФИО_СТУДЕНТА}
\def\@TeacherName{ФИО_ПРЕПОДАВАТЕЛЯ}
\def\@Year{0000}


% --- Титульный лист
\renewcommand{\maketitle}{
    \begin{titlepage}
        \begin{center}
            МИНОБРНАУКИ РОССИИ \\
            СПбГЭТУ «ЛЭТИ» ИМ. В.И. УЛЬЯНОВА (ЛЕНИНА) \\
            Кафедра \@Department
        \end{center}

        \vfill

        \begin{center}
            \textbf{
                \MakeUppercase{Отчёт} \\
                По \@WorkType \\
                По дисциплине «\@Discipline» \\
                Тема: \MakeUppercase{\@WorkTitle} \\
            }
        \end{center}

        \vfill

        \noindent
        \begin{tabularx}{\textwidth}{l X r}
            Студент гр. \@Group, вар. \@Variant & \hrulefill & \@StudentName \\\\
            Преподаватель    & \hrulefill & \@TeacherName
        \end{tabularx}

        \vfill

        \begin{center}
            Санкт-Петербург \\
            \@Year \\
        \end{center}
        \thispagestyle{empty}
    \end{titlepage}
    \newpage
    \setcounter{page}{2}
}

\endinput