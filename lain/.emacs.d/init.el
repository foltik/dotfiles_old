;; Needs to be commented or else it will be added back
; (package-initialize)

(defvar jf-config-file (expand-file-name "config.org" user-emacs-directory))
(defvar jf-init-file (expand-file-name "init.el" user-emacs-directory))
(defvar jf-load-path (expand-file-name "lisp/" user-emacs-directory))
(defvar jf-gc-threshold 20000000) ; 20MB up from 800KB

(defun jf-inhibit-gc ()
  (setq gc-cons-threshold most-positive-fixnum))
(defun jf-resume-gc ()
  (setq gc-cons-threshold jf-gc-threshold))


(message "-> Initializing Electronic Macs...")

;; Don't garbage collect during init
(jf-inhibit-gc)
(org-babel-load-file jf-config-file)
(jf-resume-gc)

(message "-> Initialized in %s with %d GCs."
	 (float-time (time-subtract after-init-time before-init-time))
	 gcs-done)
