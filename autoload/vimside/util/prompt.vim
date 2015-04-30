" Taken from eclim vim plugin

function vimside#util#prompt#ShowPrompt(prompt, list)
   no elements, no prompt
  if empty(a:list)
    return -1
  endif

  " only one element, no need to choose.
  if len(a:list) == 1
    return 0
  endif

  let prompt = ""
  let index = 0
  for item in a:list
    let prompt = prompt . index . ") " . item . "\n"
    let index = index + 1
  endfor
  let maxindex = index - 1

  try
    " clear any previous messages
    redraw
    try
      let response = input(prompt . "\n" . a:prompt . ": ")
    catch
      " echoing the list prompt vs. using it in the input() avoids apparent vim
      " bug that causes "Internal error: get_tv_string_buf()".
      echo prompt . "\n"
      let response = input(a:prompt . ": ")
    endtry
    while response !~ '\(^$\|^[0-9]\+$\)' ||
        \ response < 0 ||
        \ response > maxindex
      let response = input("You must choose a value between " .
        \ "0" . " and " . maxindex .
        \ ". (Ctrl-C to cancel): ")
    endwhile
    return response
  finally
    "echohl None
    redraw!
  endtry
endfunction
