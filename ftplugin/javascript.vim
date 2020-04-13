let script_path = expand('<sfile>:p:h') . '/../script/webpack.js'

call webpack#load_config(script_path)
