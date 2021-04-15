#ifndef __DISPLAY
#define __DISPLAY

class Display {
public:
	virtual void show() {
	}
	virtual void move(int x, int y) { //��������  -1 0   +1 0   0 -1   0 +1 
	}
	virtual void put(int player) { // player  0  ��  other ��
	} 
	virtual void back() { // player  0  ��  other ��
	}
	virtual ~Display() = 0
	{
	}
};
#endif // !__DISPLAY

