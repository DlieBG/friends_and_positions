FROM tomcat:10.0-jdk17

WORKDIR /usr/local/tomcat

COPY FAPServer.war webapps/

EXPOSE 8080
CMD ["catalina.sh", "run"]
