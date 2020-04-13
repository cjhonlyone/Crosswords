load sumN.mat
% 和为25的3个数
index = sum(sumN25 == -1);
sumN25_3 = sumN25(1:3,(index == 3));
% 和为51的4个数 不包括1
index = sum(sumN51 == -1);
sumN51_4 = sumN51(1:4,(index == 4));
sumN51_4 = sumN51_4(:,(sumN51_4(4,:) ~= 1));
% 和为51的7个数 必须包括1
index = sum(sumN51 == -1);
sumN51_7 = sumN51(1:7,(index == 1));
sumN51_7 = sumN51_7(:,(sumN51_7(7,:) == 1));

clear sumN51_ sumN25_ index

% OriginalData = sumN51_4;
% FlattenedData = OriginalData(:)'; % 展开矩阵为一列，然后转置为一行。
% MappedFlattened = mapminmax(FlattenedData, 1, 0); % 归一化。
% MappedData = reshape(MappedFlattened, size(OriginalData)); % 还原为原始矩阵形式。此处不需转置回去，因为reshape恰好是按列重新排序
% imshow(MappedData)
% index = zeros(23,l);
% for i = 2:23
%     [m,n] = find(sumN51_4 == i);
%     index(i,1:length(n)) = n';
% end
index = zeros(23,length(sumN51_4));
for i = 2:23

    index(i,:) = sum(sumN51_4 == i);
end
% 从5开始
for i = 5
    for j = 2:length(index)
        
    end
end
