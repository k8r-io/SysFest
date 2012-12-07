define(['backbone','app/models/host'],
function(Backbone) {
	Hosts = Backbone.Collection.extend({
		model: Host,
		url: "/host"
	});
	return new Hosts();
});
