class GtkPackage (GnomeXzPackage):
	def __init__ (self):
		GnomeXzPackage.__init__ (self, 'gtk+',
			version_major = '2.24',
			version_minor = '13',
			configure_flags = [
				'--with-gdktarget=%{gdk_target}',
				'--prefix="%{prefix}"'
#				'--disable-cups',
			]
		)
		self.configure = './configure'
		self.gdk_target = 'x11'

		if Package.profile.name == 'darwin':
			self.gdk_target = 'quartz'
			self.sources.extend ([
				# Custom gtkrc
				'patches/gtkrc',

				#post 2.24.13 patches
				# Fix garbage content when windows are initially mapped
				'http://git.gnome.org/browse/gtk+/patch/?id=92ea94af5f1a4d0970628b58997192ccf74cab36',
				# quartz: Actually use the window background PATTERN color
				'http://git.gnome.org/browse/gtk+/patch/?id=0e42cf81f1dad319489e447c6c4e640bed2ab915',

				# smooth scrolling, scrollbars, overscroll
				'patches/gtk-scrolling/0001-Add-_gdk_quartz_window_set_needs_display_in_region.patch',
				'patches/gtk-scrolling/0002-quartz-Fix-up-gdk_draw_drawable.patch',
				'patches/gtk-scrolling/0003-gtk-paint-only-the-exposed-region-in-gdk_window_expo.patch',
				'patches/gtk-scrolling/0004-Implement-gtk-enable-overlay-scrollbars-GtkSetting.patch',
				'patches/gtk-scrolling/0005-Smooth-scrolling.patch',
				'patches/gtk-scrolling/0006-gtk-Add-a-way-to-do-event-capture.patch',
				'patches/gtk-scrolling/0007-scrolledwindow-Kinetic-scrolling-support.patch',
				'patches/gtk-scrolling/0008-gtk-paint-to-the-right-windows-in-gtk_scrolled_windo.patch',
				'patches/gtk-scrolling/0009-GtkScrolledWindow-add-overlay-scrollbars.patch',
				'patches/gtk-scrolling/0010-gtk-add-event-handling-to-GtkScrolledWindow-s-overla.patch',
				'patches/gtk-scrolling/0011-Use-gtk-enable-overlay-scrollbars-in-GtkScrolledWind.patch',
				'patches/gtk-scrolling/0012-gtk-correctly-handle-toggling-of-the-scrollbar-visib.patch',
				'patches/gtk-scrolling/0013-gtk-handle-gtk-primary-button-warps-slider-for-the-o.patch',
				'patches/gtk-scrolling/0014-Introduce-phase-field-in-GdkEventScroll.patch',
				'patches/gtk-scrolling/0015-Add-hack-to-lock-flow-of-scroll-events-to-window-whe.patch',
				'patches/gtk-scrolling/0016-Introduce-a-background-window.patch',
				'patches/gtk-scrolling/0017-Make-scrolled-window-work-well-with-Mac-touchpad.patch',
				'patches/gtk-scrolling/0018-Use-start-end-phase-in-event-handling.patch',
				'patches/gtk-scrolling/0019-Improve-overshooting-behavior.patch',
				'patches/gtk-scrolling/0020-Cancel-out-smaller-delta-component.patch',
				'patches/gtk-scrolling/0021-quartz-Add-a-dummy-NSView-serving-as-layer-view.patch',
				'patches/gtk-scrolling/0022-gtk-port-overlay-scrollbars-to-native-CALayers.patch',
				'patches/gtk-scrolling/0023-Refrain-from-starting-fading-out-while-a-gesture-is-.patch',
				'patches/gtk-scrolling/0024-Add-weak-references-on-the-cached-event-and-pointer-.patch',
				'patches/gtk-scrolling/0025-gtk-don-t-show-the-olverlay-scrollbars-if-only-the-s.patch',
				'patches/gtk-scrolling/overlay-scrollbar-makefile-patch.diff',

				# make new modifier behviour opt-in, so as not to break old versions of MonoDevelop
				'patches/gdk-quartz-set-fix-modifiers-hack-v3.patch',

				# attempt to work around 2158 - [GTK] crash triggering context menu
				# also prints some warnings that may help to debug the real issue
				'https://bugzilla.xamarin.com/attachment.cgi?id=1644',

				# Backport of gdk_screen_get_monitor_workarea
				# Tooltip etc now honor menu and dock when positioning
				'patches/gtk-monitor-workarea.patch',

				# Embedded NSViews
				'patches/gtk-embedded-nsview/0001-gtk-add-new-widget-GtkNSView-which-alows-to-embed-an.patch',
				'patches/gtk-embedded-nsview/0002-quartz-return-events-on-embedded-foreign-NSViews-bac.patch',
				'patches/gtk-embedded-nsview/0003-gdk-add-signal-GdkWindow-native-child-event.patch',
				'patches/gtk-embedded-nsview/0004-tests-add-a-GtkEntry-to-testnsview-so-we-can-test-fo.patch',
				'patches/gtk-embedded-nsview/0005-gtk-connect-to-GdkWindow-native-child-event-to-imple.patch',
				'patches/gtk-embedded-nsview/fix-for-embedded-nsviews.patch',

				# Zoom, rotate, swipe events
				'patches/gtk-gestures.patch',

				# Bug 2158 - [GTK] crash in find_window_for_ns_event
				'https://bugzilla.xamarin.com/attachment.cgi?id=2717',

				# Bug 6156 - [gtk] Quitting the application with unsaved file and answering Cancel results in crash
				'https://bugzilla.xamarin.com/attachment.cgi?id=2214',

				# Bug 3457 - [GTK] Support more standard keyboard shortcuts in dialogs
				'https://bugzilla.xamarin.com/attachment.cgi?id=2240',

				# BXC 7465 - user is unable to click 'Breakpoint properties' option after right clicking on
				#     breakpoint circle when break point is set on last line
				# BGO 672193 - windows (including menus) shown multiple times don't get enter event if under mouse
				'http://bugzilla-attachments.gnome.org/attachment.cgi?id=228303',

				# BXC 6830 - no cursor in the search textfield
				'patches/gtk-show-retina-cursor.patch',
			])

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (2, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

	def install(self):
		Package.install(self)
		if Package.profile.name == 'darwin':
			self.install_gtkrc ()

	def install_gtkrc(self):
		origin = os.path.join (self.package_dest_dir (), os.path.basename (self.sources[1]))
		destdir = os.path.join (self.prefix, "etc", "gtk-2.0")
		if not os.path.exists (destdir):
			os.makedirs(destdir)
		self.sh('cp %s %s' % (origin, destdir))

GtkPackage ()
