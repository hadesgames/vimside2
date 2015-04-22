let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\' )

function! vimside#Enable()
  call s:SetUpPython()
endfunction

function! s:SetUpPython()
  py import vim
  py import sys

  exe 'python sys.path.insert(0, "' . s:script_folder_path . '/../python" )'
  exe 'python sys.path.insert(0, "' . s:script_folder_path . '/../third_party" )'
endfunction