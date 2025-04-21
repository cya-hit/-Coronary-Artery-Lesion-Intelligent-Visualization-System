# Coronary-Artery-Lesion-Intelligent-Visualization-System
# 冠状动脉病变智能可视化系统

This system is composed of a Vue front - end, a Flask back - end, and a deep learning model. For data storage and asynchronous communication with the deep learning model, MySQL and Redis middleware are utilized. You can experience this system by visiting http://111.42.74.240:7860/#/login. By inputting the original CT DICOM acquisition data of patients here, it is possible to carry out the segmentation and 3D reconstruction of the aorta, coronary arteries, calcified/non - calcified plaques, stents, occluded segments, and thrombi. The processing speed for one case of patient data is within 5 minutes.  
The system has been deployed for actual use in hospitals and has provided services over 100 times!

这是一个由vue前端，flask后端，和深度学习模型构成的系统，数据存储和深度学习模型异步通讯用到了MySQL和Redis中间件。
你可以通过http://111.42.74.240:7860/#/login 来体验这个系统。
这里输入病人的CT dicom原始采集数据，即可进行主动脉、冠脉、钙化/非钙化斑块、支架、阻塞段、血栓的分割和三维重建。
一例病人数据的处理速度在5min以内。  
目前该系统已经部署到医院实际使用，提供服务百余次！
![image](https://github.com/user-attachments/assets/f0820fb3-a1c0-44a2-8fde-15c3e93bd43a)
![image](https://github.com/user-attachments/assets/e7eb1bba-7ec1-468d-9754-77d8912c706f)
![image](https://github.com/user-attachments/assets/f7c7709d-bea8-4836-8209-faa92358a097)
![image](https://github.com/user-attachments/assets/15e4b75a-3788-4790-ab2c-700265d6954d)
![image](https://github.com/user-attachments/assets/82291670-120b-4433-8689-35884db9a96d)
![image](https://github.com/user-attachments/assets/26a5dcee-6cf2-458c-a140-08b6cd3148d2)


