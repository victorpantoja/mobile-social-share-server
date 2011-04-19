default_run_options[:pty] = true
set :application, "mss"
set :repository,  "git@github.com:victorpantoja/mobile-social-share-server.git"

set :scm, "git"
set :user, "victor"

set :branch, "master"

set :deploy_via, :remote_cache
set :deploy_to, "/usr/local/projetos/#{application}"

role :app, "myalbumshare.com"                          # This may be the same as your `Web` server
role :db,  "myalbumshare.com", :primary => true # This is where Rails migrations will run

