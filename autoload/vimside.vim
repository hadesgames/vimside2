let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\' )

function! vimside#Enable()
  call s:SetUpPython()
  call s:SetUpKeyBindings()
endfunction

function! s:SetUpPython()
  py import vim
  py import sys

  exe 'python sys.path.insert(0, "' . s:script_folder_path . '/../python" )'
  exe 'python sys.path.insert(0, "' . s:script_folder_path . '/../third_party" )'

  py import vimside.env
  py import vimside.command
  exe 'python vimside.env.getEnv().cwd="' . getcwd() . '"'
endfunction


function! s:SetUpKeyBindings()
  nmap <silent> <Leader>vs :call vimside#command#server#StartEnsime()<CR>

  augroup VIMSIDE_STOP
    au!
    autocmd VimLeave * call vimside#command#server#StopEnsime()
    " autocmd VimLeave scala call vimside#StopEnsime()
  augroup END
endfunction


