clear
close all
f_c=3.5*10^9;% gdy odleglosc lambda/2- niezalezne od czestotliwosci
c=3*10^8;
d= 0.02;%c/f_c/2;% odleglosc miedzy elementmi antenowymi c=lambda*f
L=16;%liczba elementow antenowych

set_TX = -15:0;
set_RX = 0:80;
B = [];
params = []; % Array to store [Tx, Rx, Rotation] for each row

% Define your rotation values
rotations = [0, pi/2, pi, 3*pi/2];

for i = 1:length(set_TX)
    % Base ideal precoder
    prekoder_ideal = exp(1j*2*pi*f_c/c*d*([0:L-1]*sind(set_TX(i)) + sind(set_RX')*[0:L-1]));

    % Loop through the 4 rotations instead of writing it out 4 times
    for r = 1:length(rotations)
        rot_val = rotations(r);
        prekoder_binary = real(prekoder_ideal * exp(1j*rot_val)) < 0;

        % Append the binary precoder to B
        B = [B; prekoder_binary];

        % Track the parameters for these specific rows
        num_rows = size(prekoder_binary, 1); % This equals length(set_RX)

        current_tx = repmat(set_TX(i), num_rows, 1); % Tx is the same for this batch
        current_rx = set_RX(:);                      % Rx varies row-by-row
        current_rot = repmat(rot_val, num_rows, 1);  % Rotation is the same for this batch

        % Append the parameters [Tx, Rx, Rotation] to our tracking array
        params = [params; current_tx, current_rx, current_rot];
    end
end

% 'ic' contains the index of the unique row that each original row maps to.
[BB, ~, ic] = unique(B, 'rows');

num_unique = size(BB, 1);

% Preallocate cell arrays to hold lists of varying lengths
Tx_lists = cell(num_unique, 1);
Rx_lists = cell(num_unique, 1);
Rot_lists = cell(num_unique, 1);

% Loop through each unique precoder to gather its parameters
for k = 1:num_unique
    % Find all row indices in the original 'B' that match this unique row 'k'
    idx = (ic == k);

    % Extract all matching parameters
    matching_params = params(idx, :);

    % Store them as arrays (transposed to row vectors like [20, 45])
    Tx_lists{k}  = unique(matching_params(:, 1)');
    Rx_lists{k}  = unique(matching_params(:, 2)');
    Rot_lists{k} = unique(matching_params(:, 3)');
end

% ---------------------------------------------------------
% SAVING THE DATA IN CUSTOM BRACKET FORMAT
% ---------------------------------------------------------

% Open a CSV file for writing
fid = fopen('codebook_test.csv', 'w');

% Write the header row
%fprintf(fid, 'Precoder;Parameters_List\n');

for k = 1:num_unique
    % 1. Format the Precoder String
    % (Keeping your previous 16x repetition rule)
    bb_row = BB(k, :);
    bb_repeated = repmat(bb_row, 1, 16);
    bb_str = sprintf('%d', bb_repeated); % Continuous string of 1s and 0s

    % 2. Get all original parameters that created this unique precoder
    idx = (ic == k);
    matching_params = params(idx, :); % This is an N x 3 matrix
    num_matches = size(matching_params, 1);

    % 3. Build the [[Tx, Rx, Rot], ...] string
    % Preallocate a cell array to hold each [Tx, Rx, Rot] string
    param_cells = cell(1, num_matches);

    for m = 1:num_matches
        % Format a single triplet as [Tx, Rx, Rotation]
        % Note: Using %g for rotation in case it has decimal values like pi/2
        param_cells{m} = sprintf('[%g, %g, %g]', ...
            matching_params(m, 1), ...
            matching_params(m, 2), ...
            rad2deg(matching_params(m, 3)));
    end

    % Join all the individual brackets with a comma and space
    joined_inner_brackets = strjoin(param_cells, ', ');

    % Wrap the entire sequence in outer brackets
    final_param_str = ['[', joined_inner_brackets, ']'];

    % 4. Write the line to the CSV separated by a semicolon
    fprintf(fid, '%s;%s\n', bb_str, final_param_str);
end
fprintf("CB DONE")
% Close the file
fclose(fid);
