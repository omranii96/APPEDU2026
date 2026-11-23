/**
 * CHARMED PARIS — enregistrement des blocs dynamiques charmed/* dans l'éditeur.
 * Aperçu = rendu serveur (ServerSideRender) ; panneau de réglages généré depuis les attributs
 * déclarés en PHP (inc/blocks.php). Aucun build : wp.element.createElement, ES2018.
 */
(function (wp, data) {
	'use strict';
	if (!wp || !wp.blocks || !data) { return; }

	var el = wp.element.createElement;
	var InspectorControls = wp.blockEditor.InspectorControls;
	var useBlockProps = wp.blockEditor.useBlockProps;
	var PanelBody = wp.components.PanelBody;
	var TextControl = wp.components.TextControl;
	var ToggleControl = wp.components.ToggleControl;
	var ServerSideRender = wp.serverSideRender;

	(data.blocks || []).forEach(function (def) {
		if (wp.blocks.getBlockType(def.name)) { return; }
		wp.blocks.registerBlockType(def.name, {
			apiVersion: 3,
			title: def.title,
			description: def.description,
			icon: def.icon,
			category: 'theme',
			attributes: def.attributes,
			supports: { html: false, align: ['wide', 'full'] },
			edit: function (props) {
				var fields = Object.keys(def.attributes).map(function (key) {
					var type = def.attributes[key].type;
					var label = def.labels[key] || key;
					var value = props.attributes[key];
					var set = function (v) { var o = {}; o[key] = v; props.setAttributes(o); };
					if (type === 'boolean') {
						return el(ToggleControl, { key: key, label: label, checked: !!value, onChange: set, __nextHasNoMarginBottom: true });
					}
					if (type === 'number') {
						return el(TextControl, { key: key, label: label, type: 'number', value: value, onChange: function (v) { set(parseInt(v, 10) || 0); }, __nextHasNoMarginBottom: true });
					}
					return el(TextControl, { key: key, label: label, value: value || '', onChange: set, __nextHasNoMarginBottom: true });
				});
				return el('div', useBlockProps(),
					fields.length ? el(InspectorControls, null, el(PanelBody, { title: (data.i18n && data.i18n.settings) || 'Settings' }, fields)) : null,
					el(ServerSideRender, { block: def.name, attributes: props.attributes })
				);
			},
			save: function () { return null; }
		});
	});
})(window.wp, window.charmedBlocks);
