clear
close all
%% GEneracja prekodera grupujacego fazy per azymut

%Patterns_limited_rotations - zmienna gdzie jest ksiazka kodowa do testow.

f_c=5.53*10^9;% gdy odleglosc lambda/2- niezalezne od czestotliwosci
c=3*10^8;
d=0.02;%c/f_c/2;% odleglosc miedzy elementmi antenowymi c=lambda*f
L=16;%liczba elementow antenowych
vector_elements=[0:L-1];%[-L/2+1:L/2];%vector_elements;

%%--------------------------Parametry------------------------%%

TX_angle=45;%-48;%[0:90]; PARAMETR
set_RX=[-90:0];%[-90:90];% PARAMETR


ile_phase_rotations=6; % PARAMETR- z modelu wyszlo, ze uzycie 6 ogranicza sredni AF o 0.1dB


ile_patternow_moze_sie_powtarzac=0; % minimum 0 -wygeneruje najmniejsza ksiazke (wystarczy ze jedna rotacja jest taka sama i juz wybiera tylko jeden z tych azymutow.
%-------------------------------------------------------------%
%% KOD
% Maksimum= inf- doda wszystkie katy z set_RX jesli sie choc troche roznia . Azymuty rozne
% -1: jesli wszystkie patterny sie powtarzaja z jednym z innych katow to
% nie dodaje kolejnego
set_phi_s=[0:359]';
katy_RX_uzyte={};
Patterny={};
maks_rotacji_per_azymut=[];
for i=1:length(set_RX)
    prekoder_ideal_ref=exp(1j*2*pi*f_c/c*d*(vector_elements*sind(TX_angle)+sind(set_RX(i))*vector_elements));
    patter_ref0=real(exp(1j*set_phi_s/360*2*pi)*prekoder_ideal_ref)>0;
    [pattern_ref]=unique(patter_ref0,'rows','stable'); % liczba unikalnych rotacji x Liczba elementow RISa
    maks_rotacji_per_azymut=[maks_rotacji_per_azymut size(pattern_ref,1)];
    add_this_RX_angle=1;
    for j=1:length(Patterny)
        [common_patterns,a,b]=intersect(pattern_ref, Patterny{j}, 'rows');
        if ile_patternow_moze_sie_powtarzac==-1

            if size(common_patterns,1)==min(size(pattern_ref,1),size(Patterny{j},1))
                add_this_RX_angle=0;
                katy_RX_uzyte{j}(end+1)=set_RX(i);
                break
            end
        else
            if size(common_patterns,1)>=ile_patternow_moze_sie_powtarzac+1 % ile obrotow musi byc identycznych zeby nie dodawac i-tego minimum: 1 (najmniejszy zbior katow), maksimum np. 32 (najwiekszy zbior katow)
                add_this_RX_angle=0;
                katy_RX_uzyte{j}(end+1)=set_RX(i);
                % zapisac kat powiazany z j do katy uzyte
                
                % if set_RX(i)==-40
                %     bb=20*log10(abs((2*pattern_ref-1)*exp(-1j*2*pi*f_c/c*d*(vector_elements'*sind(TX_angle)+sind(set_RX(i))*vector_elements'))));
                %     cc=20*log10(abs((2*Patterny{j}-1)*exp(-1j*2*pi*f_c/c*d*(vector_elements'*sind(TX_angle)+sind(set_RX(i))*vector_elements'))));
                % plot(bb)
                % hold
                % plot(cc)
                % g=0;
                % end
                break
            end
        end
    end
    if add_this_RX_angle==1
        Patterny{end+1}=pattern_ref;
        katy_RX_uzyte{end+1}=set_RX(i);
    end
end

% Patterny z ograniczonymi rotacjami

Patterns_limited_rotations={};
Patterns_limited_rotations_mat=[];
Rotations_limited={}; 

set_phi_s2=[0:360/6:359]';
Total_codebook_size=0;
for i=1:length(Patterny)
    prekoder_ideal_ref=exp(1j*2*pi*f_c/c*d*(vector_elements*sind(TX_angle)+sind(katy_RX_uzyte{i}(1))*vector_elements));
    patter_ref0=real(exp(1j*set_phi_s2/360*2*pi)*prekoder_ideal_ref)>0;
    
    [pattern_ref, ia] = unique(patter_ref0,'rows','stable'); 
    
    surviving_rotations = set_phi_s2(ia); 
    
    Total_codebook_size=Total_codebook_size+size(pattern_ref,1);
    
    Patterns_limited_rotations{end+1}=pattern_ref;
    Patterns_limited_rotations_mat=[Patterns_limited_rotations_mat; pattern_ref];
    Rotations_limited{end+1}=surviving_rotations; 
end

% ---------------------------------------------------------
% SAVING THE DATA IN CUSTOM BRACKET FORMAT
% ---------------------------------------------------------

fid = fopen('Arranged_codebook.csv', 'w');
%fprintf(fid, 'Precoder;Parameters_List\n');

% Loop through the 11 groups
for i = 1:length(Patterns_limited_rotations)
    
    % Extract the data for this specific group
    current_precoders = Patterns_limited_rotations{i}; % The unique binary matrices
    current_rotations = Rotations_limited{i};          % The phi angles for these matrices
    current_rx_list   = katy_RX_uzyte{i};              % All Rx angles that share these precoders
    
    % Loop through each individual unique precoder in this group
    for r = 1:size(current_precoders, 1)
        
        % 1. Format the Precoder String (Repeated 16x as requested)
        bb_row = current_precoders(r, :);
        bb_repeated = repmat(bb_row, 1, 16);
        bb_str = sprintf('%d', bb_repeated); 
        
        % 2. Get the specific rotation for this row
        rot_val = current_rotations(r);
        
        % 3. Build the [[Tx, Rx, Rot], ...] string for ALL matching Rx values
        num_rx = length(current_rx_list);
        param_cells = cell(1, num_rx);
        
        for m = 1:num_rx
            rx_val = current_rx_list(m);
            % Build individual triplet: [Tx, Rx, Rotation]
            param_cells{m} = sprintf('[%g, %g, %g]', TX_angle, rx_val, rot_val);
        end
        
        % Glue all the triplets together with commas
        joined_brackets = strjoin(param_cells, ', ');
        
        % Wrap the entire sequence in outer brackets
        final_param_str = ['[', joined_brackets, ']'];
        
        % 4. Write to file
        fprintf(fid, '%s;%s\n', bb_str, final_param_str);
    end
end

fclose(fid);