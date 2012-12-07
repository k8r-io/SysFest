
requirejs.config({
	shim: {
		
		backbone: {
			deps: ['underscore', 'jquery'],
			exports: 'Backbone'
		}
	},
	baseUrl: 'static/js/lib',
	paths: {
		app: '../app',
		underscore: 'lodash'
	},
	urlArgs: "bust="+(new Date()).getTime()
});

requirejs(['backbone','app/views/list','app/models/hosts'],
function (Backbone) {

	var AppRouter = Backbone.Router.extend({
		routes:{
			'': 'listHosts',
			'/host/:hostname': 'getHost'
		}
	});


	var app_router = new AppRouter();

	app_router.on('route:listHosts', function(actions){
		var hostList,hosts = new Hosts();
		var p = hosts.fetch();
		p.done(function(){
			hostList = new HostListView({el: $('#main_display')});
			hostList.render(hosts.toArray());
		}); 
	});

	app_router.on('route:getHost', function(hostname){
		var host = new Host(hostname);
	}); 
	


	Backbone.history.start();
});


