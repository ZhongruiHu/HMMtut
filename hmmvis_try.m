function [] = hmmvis(tr,e,s)
% HMMVIS displays a Matlab HMM
%     HMMVIS(TR,E,S)
%         TR = transitions    %tr = ([.3 .3 .4; .2 .2 .6; .4, .4, .2]);
%         E  = emissions      %e = ([.4, .6; .9 .1; .5, .5]);
%         S  = alphabet       %s = 'ab';
% Graphvis must also be installed.
% WARNING: this is kludgy and not platform-independent!
%
% Mike Hammond, U. of Arizona, 10/14

%% error checking
%get sizes of inputs
[eheight ewidth] = size(e);
[trheight trwidth] = size(tr);
%check that transition matrix is square
if trheight ~= trwidth
    error('transition matrix isn''t square');
end
%check that emissions matrix has the right number of states
if trheight ~= eheight
    error('emissions matrix has the wrong number of states');
end
%check that alphabet matches number of emissions
if ewidth ~= length(s)
    error('alphabet has the wrong length');
end

%% write HMM to temp dot file
%location of temp dot file
tmpFile = 'bznorkTMP.dot';
%open temp dot file
TF = fopen(tmpFile,'w');
%beginning of hmm
fprintf(TF,'digraph G {\n\trankdir = LR;\n\tq0 [style=invis,area=.2];\n');
%states and emissions
for i = 1:eheight
    fprintf(TF,'\tq%d [label="q%d',i,i);
    for j = 1:ewidth
        fprintf(TF,'\\n%c=%1.2f',s(j),e(i,j));
    end
    fprintf(TF,'"];\n');
end
%arrow for start state
fprintf(TF,'\tq0 -> q1;\n');
%state transitions
for i = 1:trheight
    for j = 1:trwidth
        fprintf(TF,'\tq%d -> q%d [label="%1.2f"];\n',i,j,tr(i,j));
    end
end
%finish hmm
fprintf(TF,'}\n');
%close temp dot file
fclose(TF);

%% convert to pdf and display
%run dot
!/usr/local/bin/dot -Tpdf bznorkTMP.dot > bznorkTMP.pdf
%open pdf
!open bznorkTMP.pdf
