clear; close all force; clc;      %limpa todas a variaveis; fecha todos os plots; limpa o terminal

%--------inicializaçao tabelas----------

%txtFile = load('testeGPS1_22_02.txt');
%csvwrite('testeGPS1_22_02.txt', txtFile);


table = readtable("F:\TST03.CSV");    %abre o aqruivo como um objeto dentro do MatLab
%t1 = table('Size',[8 4],'VariableTypes',varTypes,'VariableNames',varNames);    %tabela p/ guardar as variaveis de cada tabela

toDelete = table.RPM == -1;
table(toDelete,:) = [];

scatter(table.Latitude(:),table.Longitude(:),[],table.RPM(:),'filled')	%plota em scatter 
    colorbar	%mostra a barra de cores
    colormap default	%define o mapa de cores
    daspect([1 1 1]);	%ajeita o aspect ratio em relaçao aos dados 1:1

    xlabel('Latitude')
    ylabel('Longitude')
    title('GPS')
    
    grafico = geoscatter(table,"Latitude","Longitude",'filled');
    geobasemap satellite
    grafico.ColorVariable = "RPM";
    c = colorbar;
    c.Label.String = "RPM";
    
%figure

% plot(smoothdata(txtFile(:,6)))
% hold on
% yyaxis right
% plot(smoothdata(txtFile(:,2)))

% plot(table.Tempo(1:3000)/1000,table.VelocidadeDianteira(1:3000))
% hold on
% yyaxis right
% plot(table.Tempo(1:3000)/1000,table.RPM(1:3000))