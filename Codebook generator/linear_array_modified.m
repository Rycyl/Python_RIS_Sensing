clear
close all
f_c = 5.53*10^9; % gdy odleglosc lambda/2- niezalezne od czestotliwosci
c = 299792458;
d = 0.02; %c/f_c/2; % odleglosc miedzy elementmi antenowymi c = lambda*f
L = 16;%liczba elementow antenowych

kat_TX = -48 % od 0 do 90; 0 =  na wprost RISa
kat_RX = 40 %od 0 do -90 najsensowniejsze; 0 =  na wprost RISa

kanal_do_od_RIS = exp(-1j*2*pi*f_c/c*d*([-8:7]*sind(kat_TX)+[-8:7]*sind(kat_RX)));[L-1:-1:0]
prekoder = conj(kanal_do_od_RIS);

katy_pomiarowe_RX = [-90:90];

AF = exp(-1j*2*pi*f_c/c*d*([-8:7]*sind(kat_TX)+sind(katy_pomiarowe_RX')*[-8:7]))*transpose(prekoder);

plot(katy_pomiarowe_RX,10*log10(abs(AF).^2),'--', "linewidth",3)
hold on

prekoder_bin = 2*(real(prekoder*exp(1j*0*pi/2))>0)-1;
AF = exp(-1j*2*pi*f_c/c*d*([-8:7]*sind(kat_TX)+sind(katy_pomiarowe_RX')*[-8:7]))*transpose(prekoder_bin);
plot(katy_pomiarowe_RX,10*log10(abs(AF).^2), "linewidth",3)
prekoder_bin = 2*(real(prekoder*exp(1j*1*pi/2))>0)-1;
AF = exp(-1j*2*pi*f_c/c*d*([-8:7]*sind(kat_TX)+sind(katy_pomiarowe_RX')*[-8:7]))*transpose(prekoder_bin);
plot(katy_pomiarowe_RX,10*log10(abs(AF).^2), "linewidth",3)
leg = legend ("Accurate", "Binary", "Binary rotated");
xticks(-90:10:90);
yticks(-10:5:30);
set(gca, "linewidth", 1, "fontsize", 20)
legend(leg, "location", "north","orientation", "horizontal")
xlabel('RX localisation [°]')
ylabel('AF (dB)')
% title(['AF for TX at ' num2str(kat_TX) ' and RIS pattern for TX angle = ' num2str(kat_TX) ' and RX angle = ' num2str(kat_RX)])
prekoder_bin = 2*(real(prekoder*exp(1j*2*pi/2))>0)-1;

grid
figure
set_RX = [-90:90];
prekoder_ideal = exp(1j*2*pi*f_c/c*d*([-8:7]*sind(kat_TX)+sind(set_RX')*[-8:7]));%
prekoder_binary = zeros(length(set_RX),L);
prekoder_binary(real(prekoder_ideal)<0) = 1;
subplot(1,3,1)
pcolor([-8:7],set_RX,angle(prekoder_ideal))
title(['optimal angle of precoder \newline for TX at' num2str(kat_TX)])
xlabel('RIS element index')
ylabel('RX azimuth')
subplot(1,3,2)
pcolor([-8:7],set_RX,prekoder_binary)
prekoder_binary2 = zeros(length(set_RX),L);
prekoder_binary2(real(prekoder_ideal*exp(1j*pi/2))<0) = 1; % jak zakladamy, ze do odbiornika dociera suma odbicia od
title(['binary patter \newline for TX at ' num2str(kat_TX)])
xlabel('RIS element index')
ylabel('RX azimuth')
% RIS i innych sciezek, to odbicie od RISa moze byc okrecone o jakis staly kat (tu 90 stopni),
% zeby byl w fazie tego bezposredniego.
subplot(1,3,3)
pcolor([-8:7],set_RX,prekoder_binary2)
title(['binary pattern pi/2 rotated \newline for TX at' num2str(kat_TX)])
AA = unique(prekoder_binary2,'rows'); % 67
A = unique(prekoder_binary,'rows');

AAA = unique([AA;A;~AA;~A],'rows'); %obroty o 90 stopnia

%zbior dla wszystkich odbiorczych i nadawczych
set_TX = [0:90];
set_RX = [-90:90];
B = [];
for i = 1:length(set_TX)
prekoder_ideal = exp(1j*2*pi*f_c/c*d*([-8:7]*sind(set_TX(i))+sind(set_RX')*[-8:7]));
prekoder_binary = real(prekoder_ideal)<0;
B = [B;prekoder_binary];
prekoder_binary = real(prekoder_ideal*exp(1j*pi/2))<0;
B = [B;prekoder_binary];
prekoder_binary = real(prekoder_ideal*exp(1j*pi))<0;
B = [B;prekoder_binary];
prekoder_binary = real(prekoder_ideal*exp(1j*3*pi/2))<0;
B = [B;prekoder_binary];
end
BB = unique(B,'rows');

rows_to_keep=ones(1,size(BB,1));
for i=1:size(BB,1)-1% probably not optimal removal
    for ii=i+1:size(BB,1)
        if rows_to_keep(i)==1 && sum(xor(BB(i,:),BB(ii,:)))<=2 % hamming distance to remove
            rows_to_keep(ii)=0;
        end
    end
end
CC=BB(logical(rows_to_keep),:);
c=0;





