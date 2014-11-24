\NeedsTeXFormat{LaTeX2e}[1994/12/01]
\ProvidesClass{report}[2001/05/28 Document Report]

\LoadClass[a4paper,8pt]{article}
\RequirePackage[top=2cm,bottom=2cm,left=1cm,right=1cm,landscape]{geometry}
\RequirePackage{graphicx}
\RequirePackage{fancyhdr}

\setlength{\headwidth}{\textwidth}
\setlength{\headheight}{2cm}
\pagestyle{fancy}
\fancyhf{}

\newcommand{\logo}[1]{
\fancyhead[L]{ #1 }
}

\newcommand{\name}[1]{
\fancyhead[R]{ #1 }
}

