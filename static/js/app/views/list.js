define(['jquery','backbone','text!app/templates/list.html'],
function($,Backbone,template) {
	HostListView = Backbone.View.extend({
		initialize: function(){
		},
		render: function(hosts){
			this.template = _.template( template, {collection: hosts} );
		
			this.$el.html(this.template);
		}
	});
	return new HostListView();
});
