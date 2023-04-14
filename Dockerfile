FROM tomcat:10.1.7-jre17

COPY FAPServer1_v23028.war /usr/local/tomcat/webapps/FAPServer.war

EXPOSE 8080
CMD ["catalina.sh", "run"]