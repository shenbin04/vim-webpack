function! s:parse_webpack_config(job_id, data, event_type)
  try
    let resolve = json_decode(join(a:data, "\n"))
    let b:webpack_resolve = resolve
    for module in resolve.modules
      execute 'setlocal path+=' . module
    endfor
  catch
  endtry
endfunction

function! webpack#load_config(script_path)
  let cmd = 'node'
  let config = findfile('webpack.config.js', '.;')
  if empty(config)
    let config = findfile('webpack.config.babel.js', '.;')
    let cmd = 'npx babel-node'
  endif

  if len(config)
    let jobid = async#job#start(['bash', '-c', 'NODE_PATH=. ' . cmd . ' ' . a:script_path . ' ' . fnamemodify(config, ':p')], {
          \ 'on_stdout': function('s:parse_webpack_config'),
          \ })
  endif
endfunction
