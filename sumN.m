load sumN.mat
% ��Ϊ25��3����
index = sum(sumN25 == -1);
sumN25_3 = sumN25(1:3,(index == 3));
% ��Ϊ51��4���� ������1
index = sum(sumN51 == -1);
sumN51_4 = sumN51(1:4,(index == 4));
sumN51_4 = sumN51_4(:,(sumN51_4(4,:) ~= 1));
% ��Ϊ51��7���� �������1
index = sum(sumN51 == -1);
sumN51_7 = sumN51(1:7,(index == 1));
sumN51_7 = sumN51_7(:,(sumN51_7(7,:) == 1));

clear sumN51_ sumN25_ index

% OriginalData = sumN51_4;
% FlattenedData = OriginalData(:)'; % չ������Ϊһ�У�Ȼ��ת��Ϊһ�С�
% MappedFlattened = mapminmax(FlattenedData, 1, 0); % ��һ����
% MappedData = reshape(MappedFlattened, size(OriginalData)); % ��ԭΪԭʼ������ʽ���˴�����ת�û�ȥ����Ϊreshapeǡ���ǰ�����������
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
% ��5��ʼ
for i = 5
    for j = 2:length(index)
        
    end
end
