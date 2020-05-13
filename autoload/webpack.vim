let s:webpack_resolves = {}
let s:config = ''

function! s:use_webpack_resolve(resolve)
  let b:webpack_resolve = a:resolve
  for module in a:resolve.modules
    execute 'setlocal path+=' . module
  endfor
endfunction

function! s:parse_webpack_config(job_id, data, event_type)
  try
    let resolve = json_decode(join(a:data, "\n"))
    let s:webpack_resolves[s:config] = resolve
    call s:use_webpack_resolve(resolve)
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
    let resolve = get(s:webpack_resolves, config)
    if empty(resolve)
      let s:config = config
      let jobid = async#job#start(['bash', '-c', 'NODE_PATH=. ' . cmd . ' ' . a:script_path . ' ' . fnamemodify(config, ':p')], {
            \ 'on_stdout': function('s:parse_webpack_config'),
            \ })
    else
      call s:use_webpack_resolve(resolve)
    endif
  endif
endfunction
