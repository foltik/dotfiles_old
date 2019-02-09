;; Needs to be commented or else it will be added back
; (package-initialize)

(message "Initializing Electronic Macs...")
(org-babel-load-file
  (expand-file-name "config.org" user-emacs-directory))
