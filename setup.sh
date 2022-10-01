mkdir -p ~/frontend/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~frontend/.streamlit/config.toml