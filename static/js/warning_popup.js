odoo.define('appsmod2.FormViewExtension', function(require) {
	"use strict";

	var core = require("web.core");
	var FormRenderer = require("web.FormRenderer");
	var Dialog = require("web.Dialog");
	var _t = core._t;

	var monthsDifference = function(date1, date2) {
		return date2.getMonth() - date1.getMonth() + (12 * (date2.getFullYear() - date1.getFullYear()))
	}
	
	var FormViewExtension = FormRenderer.include({
		_renderView: function() {
			var self = this;
			return this._super.apply(this, arguments).then(function () {

				var last_update_date = new Date(self.state.data.__last_update);
				var today = new Date();
				var diff = monthsDifference(last_update_date, today);
				if (self.state.model == "application" && self.mode == "readonly" && diff >= 3){
					console.log("This Application has not been update since 3 moths.");
					self.do_warn(_t("Alert"), _t("This application hasn't been updated for more than three months."));
					// Dialog.alert(_t("This application hasn't been updated for more than three months."));
				}
			});
		}
	});
});