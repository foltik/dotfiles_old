;; Needs to be commented or else it will be added back
; (package-initialize)

(defvar jf-config-file (expand-file-name "sandbox.org" user-emacs-directory))
(defvar jf-init-file (expand-file-name "init.el" user-emacs-directory))
(defvar jf-load-path (expand-file-name "lisp/" user-emacs-directory))

(message "Initializing Electronic Macs...")
(org-babel-load-file jf-config-file)
