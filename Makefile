main: grant install final
grant:
	chmod a+x install.sh
install:
	bash install.sh
final:
	echo 'Installation success. Compiler is ready to use.'