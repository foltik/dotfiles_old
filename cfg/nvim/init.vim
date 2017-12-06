runtime! archlinux.vim

let g:python_host_prog  = '/usr/bin/python2.7'
let g:python3_host_prog = '/usr/bin/python3'


call plug#begin('~/.local/share/nvim/plugged')

Plug 'xolox/vim-misc'
Plug 'xolox/vim-easytags'
Plug 'jiangmiao/auto-pairs'
Plug 'scrooloose/nerdtree'
Plug 'fidian/hexmode'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'majutsushi/tagbar'

Plug 'neomake/neomake'
if has('nvim')
	Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins'  }
else
	Plug 'Shougo/deoplete.nvim'
	Plug 'roxma/nvim-yarp'
	Plug 'roxma/vim-hug-neovim-rpc'
endif

call plug#end()


filetype plugin indent on
syntax enable

" disable beeping
set noerrorbells visualbell t_vb=
if has('autocmd')
  autocmd GUIEnter * set visualbell t_vb=
endif

set laststatus=2
set showtabline=1
set noshowmode
set tabstop=4
set shiftwidth=4
set expandtab
set autoindent
set selectmode=mouse
set mouse=a
set nobackup
set nowritebackup
set history=50
set ruler
set backspace=indent,eol,start
set autoread
set wildmenu

set number
set encoding=utf-8

set incsearch " CTRL-G and CTRL-T keys to move to the next and previous match
" Use <C-L> to clear the highlighting of :set hlsearch.
if maparg('<C-L>', 'n') ==# ''
  nnoremap <silent> <C-L> :nohlsearch<C-R>=has('diff')?'<Bar>diffupdate':''<CR><CR><C-L>
endif

colorscheme SerialExperimentsLain


" Plugin configs

" Tagbar
nmap <F8> :TagbarToggle<CR>

" Airline
let g:airline_theme='simple'
let g:airline_powerline_fonts=1

" Easytags
let g:easytags_async = 1 " Might not work lmao
set tags=./tags;
let g:easytags_dynamic_files = 1 " Per-project tags files
:let g:easytags_resolve_links = 1 " Resolve hard/soft links in UNIX

" Hex editor mode
map <C-h> :Hexmode<CR> " ctrl + h
let g:hexmode_patterns = '*.bin,*.exe,*.dat,*.o,*.out'
let g:hexmode_autodetect = 1

" Nerd Tree
map <C-n> :NERDTreeToggle<CR>

" syntastic (unused)
" set statusline+=%#warningmsg#
" set statusline+=%{SyntasticStatuslineFlag()}
" set statusline+=%*
"
" let g:syntastic_always_populate_loc_list = 1
" let g:syntastic_auto_loc_list = 1
" let g:syntastic_check_on_open = 1
" let g:syntastic_check_on_wq = 0


" Neovim specific stuff below

" Neomake
function! MyOnBattery()
    if filereadable('/sys/class/power_supply/AC/online')
       return readfile('/sys/class/power_supply/AC/online') == ['0']
    endif
    return 0
endfunction

if MyOnBattery()
  call neomake#configure#automake('w')
else
  call neomake#configure#automake('nw', 1000)
endif

" deoplete
call deoplete#enable()

