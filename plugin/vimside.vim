
augroup vimsideStart
  autocmd!
  autocmd VimEnter * call vimside#Enable()
  autocmd BufNewFile,BufRead *.scala                 set filetype=scala
  autocmd FileType scala set omnifunc=vimside#command#completion#Complete
augroup END
