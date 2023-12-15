#include <stdio.h>
#include <stdlib.h>

struct Employee {
    char name[50];
    int employeeId;
    float salary;
};

void addEmployee(struct Employee* company, int* employeeCount) {
    printf("กรอกชื่อพนักงาน: ");
    scanf("%s", company[*employeeCount].name);

    printf("กรอกเลขประจำตัวพนักงาน: ");
    scanf("%d", &company[*employeeCount].employeeId);

    printf("กรอกเงินเดือน: ");
    scanf("%f", &company[*employeeCount].salary);

    (*employeeCount)++;
}
void displayEmployees(const struct Employee* company, int employeeCount) {
    printf("\nข้อมูลพนักงาน:\n");
    for (int i = 0; i < employeeCount; ++i) {
        printf("ชื่อ : %s\n", company[i].name);
        printf("เลขประจำตัว พนักงาน : %d\n", company[i].employeeId);
        printf("เงินเดือน : %.2f\n", company[i].salary);
        printf("--------------------------\n");
    }
}

int main() {
    int maxEmployees = 10;
    struct Employee* company = (struct Employee*)malloc(maxEmployees * sizeof(struct Employee));
    int employeeCount = 0;

    int choice;
    do {
        printf("ข้อมูลพนักงานในบริษัท");
        printf("\n 1. เพ่ิมข้อมูลพนักงาน \n");
        printf("2. แสดงข้อมูลพพนักงาน\n");
        printf("3. ออกจากโปรแกรม \n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                if (employeeCount < maxEmployees) {
                    addEmployee(company, &employeeCount);
                } else {
                    printf("ข้อมูลพนักงานเกินขีดจำกัดแล้ว \n");
                }
                break;
            case 2:
                displayEmployees(company, employeeCount);
                break;
            case 3:
                printf("ออกจากโปรแกรม\n");
                break;
            default:
                printf("โปรดเลือกเลขที่อยู่ในชอยส์\n");
        }
    } while (choice != 3);
    free(company);

    return 0;
}
