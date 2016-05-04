/**********************************************************************/
/*   ____  ____                                                       */
/*  /   /\/   /                                                       */
/* /___/  \  /                                                        */
/* \   \   \/                                                       */
/*  \   \        Copyright (c) 2003-2009 Xilinx, Inc.                */
/*  /   /          All Right Reserved.                                 */
/* /---/   /\                                                         */
/* \   \  /  \                                                      */
/*  \___\/\___\                                                    */
/***********************************************************************/

/* This file is designed for use with ISim build 0x7708f090 */

#define XSI_HIDE_SYMBOL_SPEC true
#include "xsi.h"
#include <memory.h>
#ifdef __GNUC__
#include <stdlib.h>
#else
#include <malloc.h>
#define alloca _alloca
#endif
static const char *ng0 = "D:/OneDrive/Projects/CS240/Lab9/blram.v";
static const char *ng1 = "D:/OneDrive/Projects/CS240/Lab9/program.v";
static unsigned int ng2[] = {268599311U, 0U};
static int ng3[] = {0, 0};
static unsigned int ng4[] = {163860U, 0U};
static int ng5[] = {1, 0};
static unsigned int ng6[] = {3221274629U, 0U};
static int ng7[] = {2, 0};
static unsigned int ng8[] = {7U, 0U};
static int ng9[] = {3, 0};
static unsigned int ng10[] = {0U, 0U};
static int ng11[] = {5, 0};
static unsigned int ng12[] = {3221274634U, 0U};
static int ng13[] = {7, 0};
static unsigned int ng14[] = {3489808384U, 0U};
static int ng15[] = {8, 0};
static unsigned int ng16[] = {8U, 0U};
static int ng17[] = {9, 0};
static unsigned int ng18[] = {20U, 0U};
static int ng19[] = {10, 0};
static unsigned int ng20[] = {2U, 0U};
static int ng21[] = {15, 0};
static unsigned int ng22[] = {3U, 0U};
static int ng23[] = {20, 0};



static void Always_14_0(char *t0)
{
    char t7[8];
    char t14[8];
    char t25[8];
    char *t1;
    char *t2;
    char *t3;
    char *t4;
    char *t5;
    char *t6;
    char *t8;
    char *t9;
    char *t10;
    char *t11;
    char *t12;
    char *t13;
    char *t15;
    char *t16;
    char *t17;
    unsigned int t18;
    unsigned int t19;
    unsigned int t20;
    unsigned int t21;
    unsigned int t22;
    unsigned int t23;
    char *t24;
    unsigned int t26;
    unsigned int t27;
    unsigned int t28;
    unsigned int t29;
    unsigned int t30;
    unsigned int t31;
    int t32;
    unsigned int t33;
    int t34;
    int t35;
    unsigned int t36;
    unsigned int t37;
    int t38;
    int t39;

LAB0:    t1 = (t0 + 3440U);
    t2 = *((char **)t1);
    if (t2 == 0)
        goto LAB2;

LAB3:    goto *t2;

LAB2:    xsi_set_current_line(14, ng0);
    t2 = (t0 + 4008);
    *((int *)t2) = 1;
    t3 = (t0 + 3472);
    *((char **)t3) = t2;
    *((char **)t1) = &&LAB4;

LAB1:    return;
LAB4:    xsi_set_current_line(14, ng0);

LAB5:    xsi_set_current_line(15, ng0);
    t4 = (t0 + 2520);
    t5 = (t4 + 56U);
    t6 = *((char **)t5);
    t8 = (t0 + 2520);
    t9 = (t8 + 72U);
    t10 = *((char **)t9);
    t11 = (t0 + 2520);
    t12 = (t11 + 64U);
    t13 = *((char **)t12);
    t15 = (t0 + 1800U);
    t16 = *((char **)t15);
    memset(t14, 0, 8);
    t15 = (t14 + 4);
    t17 = (t16 + 4);
    t18 = *((unsigned int *)t16);
    t19 = (t18 >> 0);
    *((unsigned int *)t14) = t19;
    t20 = *((unsigned int *)t17);
    t21 = (t20 >> 0);
    *((unsigned int *)t15) = t21;
    t22 = *((unsigned int *)t14);
    *((unsigned int *)t14) = (t22 & 1023U);
    t23 = *((unsigned int *)t15);
    *((unsigned int *)t15) = (t23 & 1023U);
    xsi_vlog_generic_get_array_select_value(t7, 32, t6, t10, t13, 2, 1, t14, 10, 2);
    t24 = (t0 + 2360);
    xsi_vlogvar_wait_assign_value(t24, t7, 0, 0, 32, 1000LL);
    xsi_set_current_line(16, ng0);
    t2 = (t0 + 1640U);
    t3 = *((char **)t2);
    t2 = (t3 + 4);
    t18 = *((unsigned int *)t2);
    t19 = (~(t18));
    t20 = *((unsigned int *)t3);
    t21 = (t20 & t19);
    t22 = (t21 != 0);
    if (t22 > 0)
        goto LAB6;

LAB7:
LAB8:    goto LAB2;

LAB6:    xsi_set_current_line(17, ng0);
    t4 = (t0 + 1960U);
    t5 = *((char **)t4);
    t4 = (t0 + 2520);
    t6 = (t0 + 2520);
    t8 = (t6 + 72U);
    t9 = *((char **)t8);
    t10 = (t0 + 2520);
    t11 = (t10 + 64U);
    t12 = *((char **)t11);
    t13 = (t0 + 1800U);
    t15 = *((char **)t13);
    memset(t25, 0, 8);
    t13 = (t25 + 4);
    t16 = (t15 + 4);
    t23 = *((unsigned int *)t15);
    t26 = (t23 >> 0);
    *((unsigned int *)t25) = t26;
    t27 = *((unsigned int *)t16);
    t28 = (t27 >> 0);
    *((unsigned int *)t13) = t28;
    t29 = *((unsigned int *)t25);
    *((unsigned int *)t25) = (t29 & 1023U);
    t30 = *((unsigned int *)t13);
    *((unsigned int *)t13) = (t30 & 1023U);
    xsi_vlog_generic_convert_array_indices(t7, t14, t9, t12, 2, 1, t25, 10, 2);
    t17 = (t7 + 4);
    t31 = *((unsigned int *)t17);
    t32 = (!(t31));
    t24 = (t14 + 4);
    t33 = *((unsigned int *)t24);
    t34 = (!(t33));
    t35 = (t32 && t34);
    if (t35 == 1)
        goto LAB9;

LAB10:    goto LAB8;

LAB9:    t36 = *((unsigned int *)t7);
    t37 = *((unsigned int *)t14);
    t38 = (t36 - t37);
    t39 = (t38 + 1);
    xsi_vlogvar_wait_assign_value(t4, t5, 0, *((unsigned int *)t14), t39, 1000LL);
    goto LAB10;

}

static void Initial_20_1(char *t0)
{
    char t3[8];
    char t4[8];
    char *t1;
    char *t2;
    char *t5;
    char *t6;
    char *t7;
    char *t8;
    char *t9;
    char *t10;
    char *t11;
    char *t12;
    unsigned int t13;
    int t14;
    char *t15;
    unsigned int t16;
    int t17;
    int t18;
    unsigned int t19;
    unsigned int t20;
    int t21;
    int t22;

LAB0:    xsi_set_current_line(20, ng0);

LAB2:    xsi_set_current_line(1, ng1);
    t1 = ((char*)((ng2)));
    t2 = (t0 + 2520);
    t5 = (t0 + 2520);
    t6 = (t5 + 72U);
    t7 = *((char **)t6);
    t8 = (t0 + 2520);
    t9 = (t8 + 64U);
    t10 = *((char **)t9);
    t11 = ((char*)((ng3)));
    xsi_vlog_generic_convert_array_indices(t3, t4, t7, t10, 2, 1, t11, 32, 1);
    t12 = (t3 + 4);
    t13 = *((unsigned int *)t12);
    t14 = (!(t13));
    t15 = (t4 + 4);
    t16 = *((unsigned int *)t15);
    t17 = (!(t16));
    t18 = (t14 && t17);
    if (t18 == 1)
        goto LAB3;

LAB4:    xsi_set_current_line(2, ng1);
    t1 = ((char*)((ng4)));
    t2 = (t0 + 2520);
    t5 = (t0 + 2520);
    t6 = (t5 + 72U);
    t7 = *((char **)t6);
    t8 = (t0 + 2520);
    t9 = (t8 + 64U);
    t10 = *((char **)t9);
    t11 = ((char*)((ng5)));
    xsi_vlog_generic_convert_array_indices(t3, t4, t7, t10, 2, 1, t11, 32, 1);
    t12 = (t3 + 4);
    t13 = *((unsigned int *)t12);
    t14 = (!(t13));
    t15 = (t4 + 4);
    t16 = *((unsigned int *)t15);
    t17 = (!(t16));
    t18 = (t14 && t17);
    if (t18 == 1)
        goto LAB5;

LAB6:    xsi_set_current_line(3, ng1);
    t1 = ((char*)((ng6)));
    t2 = (t0 + 2520);
    t5 = (t0 + 2520);
    t6 = (t5 + 72U);
    t7 = *((char **)t6);
    t8 = (t0 + 2520);
    t9 = (t8 + 64U);
    t10 = *((char **)t9);
    t11 = ((char*)((ng7)));
    xsi_vlog_generic_convert_array_indices(t3, t4, t7, t10, 2, 1, t11, 32, 1);
    t12 = (t3 + 4);
    t13 = *((unsigned int *)t12);
    t14 = (!(t13));
    t15 = (t4 + 4);
    t16 = *((unsigned int *)t15);
    t17 = (!(t16));
    t18 = (t14 && t17);
    if (t18 == 1)
        goto LAB7;

LAB8:    xsi_set_current_line(4, ng1);
    t1 = ((char*)((ng8)));
    t2 = (t0 + 2520);
    t5 = (t0 + 2520);
    t6 = (t5 + 72U);
    t7 = *((char **)t6);
    t8 = (t0 + 2520);
    t9 = (t8 + 64U);
    t10 = *((char **)t9);
    t11 = ((char*)((ng9)));
    xsi_vlog_generic_convert_array_indices(t3, t4, t7, t10, 2, 1, t11, 32, 1);
    t12 = (t3 + 4);
    t13 = *((unsigned int *)t12);
    t14 = (!(t13));
    t15 = (t4 + 4);
    t16 = *((unsigned int *)t15);
    t17 = (!(t16));
    t18 = (t14 && t17);
    if (t18 == 1)
        goto LAB9;

LAB10:    xsi_set_current_line(5, ng1);
    t1 = ((char*)((ng10)));
    t2 = (t0 + 2520);
    t5 = (t0 + 2520);
    t6 = (t5 + 72U);
    t7 = *((char **)t6);
    t8 = (t0 + 2520);
    t9 = (t8 + 64U);
    t10 = *((char **)t9);
    t11 = ((char*)((ng11)));
    xsi_vlog_generic_convert_array_indices(t3, t4, t7, t10, 2, 1, t11, 32, 1);
    t12 = (t3 + 4);
    t13 = *((unsigned int *)t12);
    t14 = (!(t13));
    t15 = (t4 + 4);
    t16 = *((unsigned int *)t15);
    t17 = (!(t16));
    t18 = (t14 && t17);
    if (t18 == 1)
        goto LAB11;

LAB12:    xsi_set_current_line(6, ng1);
    t1 = ((char*)((ng12)));
    t2 = (t0 + 2520);
    t5 = (t0 + 2520);
    t6 = (t5 + 72U);
    t7 = *((char **)t6);
    t8 = (t0 + 2520);
    t9 = (t8 + 64U);
    t10 = *((char **)t9);
    t11 = ((char*)((ng13)));
    xsi_vlog_generic_convert_array_indices(t3, t4, t7, t10, 2, 1, t11, 32, 1);
    t12 = (t3 + 4);
    t13 = *((unsigned int *)t12);
    t14 = (!(t13));
    t15 = (t4 + 4);
    t16 = *((unsigned int *)t15);
    t17 = (!(t16));
    t18 = (t14 && t17);
    if (t18 == 1)
        goto LAB13;

LAB14:    xsi_set_current_line(7, ng1);
    t1 = ((char*)((ng14)));
    t2 = (t0 + 2520);
    t5 = (t0 + 2520);
    t6 = (t5 + 72U);
    t7 = *((char **)t6);
    t8 = (t0 + 2520);
    t9 = (t8 + 64U);
    t10 = *((char **)t9);
    t11 = ((char*)((ng15)));
    xsi_vlog_generic_convert_array_indices(t3, t4, t7, t10, 2, 1, t11, 32, 1);
    t12 = (t3 + 4);
    t13 = *((unsigned int *)t12);
    t14 = (!(t13));
    t15 = (t4 + 4);
    t16 = *((unsigned int *)t15);
    t17 = (!(t16));
    t18 = (t14 && t17);
    if (t18 == 1)
        goto LAB15;

LAB16:    xsi_set_current_line(8, ng1);
    t1 = ((char*)((ng16)));
    t2 = (t0 + 2520);
    t5 = (t0 + 2520);
    t6 = (t5 + 72U);
    t7 = *((char **)t6);
    t8 = (t0 + 2520);
    t9 = (t8 + 64U);
    t10 = *((char **)t9);
    t11 = ((char*)((ng17)));
    xsi_vlog_generic_convert_array_indices(t3, t4, t7, t10, 2, 1, t11, 32, 1);
    t12 = (t3 + 4);
    t13 = *((unsigned int *)t12);
    t14 = (!(t13));
    t15 = (t4 + 4);
    t16 = *((unsigned int *)t15);
    t17 = (!(t16));
    t18 = (t14 && t17);
    if (t18 == 1)
        goto LAB17;

LAB18:    xsi_set_current_line(9, ng1);
    t1 = ((char*)((ng18)));
    t2 = (t0 + 2520);
    t5 = (t0 + 2520);
    t6 = (t5 + 72U);
    t7 = *((char **)t6);
    t8 = (t0 + 2520);
    t9 = (t8 + 64U);
    t10 = *((char **)t9);
    t11 = ((char*)((ng19)));
    xsi_vlog_generic_convert_array_indices(t3, t4, t7, t10, 2, 1, t11, 32, 1);
    t12 = (t3 + 4);
    t13 = *((unsigned int *)t12);
    t14 = (!(t13));
    t15 = (t4 + 4);
    t16 = *((unsigned int *)t15);
    t17 = (!(t16));
    t18 = (t14 && t17);
    if (t18 == 1)
        goto LAB19;

LAB20:    xsi_set_current_line(10, ng1);
    t1 = ((char*)((ng20)));
    t2 = (t0 + 2520);
    t5 = (t0 + 2520);
    t6 = (t5 + 72U);
    t7 = *((char **)t6);
    t8 = (t0 + 2520);
    t9 = (t8 + 64U);
    t10 = *((char **)t9);
    t11 = ((char*)((ng21)));
    xsi_vlog_generic_convert_array_indices(t3, t4, t7, t10, 2, 1, t11, 32, 1);
    t12 = (t3 + 4);
    t13 = *((unsigned int *)t12);
    t14 = (!(t13));
    t15 = (t4 + 4);
    t16 = *((unsigned int *)t15);
    t17 = (!(t16));
    t18 = (t14 && t17);
    if (t18 == 1)
        goto LAB21;

LAB22:    xsi_set_current_line(11, ng1);
    t1 = ((char*)((ng22)));
    t2 = (t0 + 2520);
    t5 = (t0 + 2520);
    t6 = (t5 + 72U);
    t7 = *((char **)t6);
    t8 = (t0 + 2520);
    t9 = (t8 + 64U);
    t10 = *((char **)t9);
    t11 = ((char*)((ng23)));
    xsi_vlog_generic_convert_array_indices(t3, t4, t7, t10, 2, 1, t11, 32, 1);
    t12 = (t3 + 4);
    t13 = *((unsigned int *)t12);
    t14 = (!(t13));
    t15 = (t4 + 4);
    t16 = *((unsigned int *)t15);
    t17 = (!(t16));
    t18 = (t14 && t17);
    if (t18 == 1)
        goto LAB23;

LAB24:
LAB1:    return;
LAB3:    t19 = *((unsigned int *)t3);
    t20 = *((unsigned int *)t4);
    t21 = (t19 - t20);
    t22 = (t21 + 1);
    xsi_vlogvar_assign_value(t2, t1, 0, *((unsigned int *)t4), t22);
    goto LAB4;

LAB5:    t19 = *((unsigned int *)t3);
    t20 = *((unsigned int *)t4);
    t21 = (t19 - t20);
    t22 = (t21 + 1);
    xsi_vlogvar_assign_value(t2, t1, 0, *((unsigned int *)t4), t22);
    goto LAB6;

LAB7:    t19 = *((unsigned int *)t3);
    t20 = *((unsigned int *)t4);
    t21 = (t19 - t20);
    t22 = (t21 + 1);
    xsi_vlogvar_assign_value(t2, t1, 0, *((unsigned int *)t4), t22);
    goto LAB8;

LAB9:    t19 = *((unsigned int *)t3);
    t20 = *((unsigned int *)t4);
    t21 = (t19 - t20);
    t22 = (t21 + 1);
    xsi_vlogvar_assign_value(t2, t1, 0, *((unsigned int *)t4), t22);
    goto LAB10;

LAB11:    t19 = *((unsigned int *)t3);
    t20 = *((unsigned int *)t4);
    t21 = (t19 - t20);
    t22 = (t21 + 1);
    xsi_vlogvar_assign_value(t2, t1, 0, *((unsigned int *)t4), t22);
    goto LAB12;

LAB13:    t19 = *((unsigned int *)t3);
    t20 = *((unsigned int *)t4);
    t21 = (t19 - t20);
    t22 = (t21 + 1);
    xsi_vlogvar_assign_value(t2, t1, 0, *((unsigned int *)t4), t22);
    goto LAB14;

LAB15:    t19 = *((unsigned int *)t3);
    t20 = *((unsigned int *)t4);
    t21 = (t19 - t20);
    t22 = (t21 + 1);
    xsi_vlogvar_assign_value(t2, t1, 0, *((unsigned int *)t4), t22);
    goto LAB16;

LAB17:    t19 = *((unsigned int *)t3);
    t20 = *((unsigned int *)t4);
    t21 = (t19 - t20);
    t22 = (t21 + 1);
    xsi_vlogvar_assign_value(t2, t1, 0, *((unsigned int *)t4), t22);
    goto LAB18;

LAB19:    t19 = *((unsigned int *)t3);
    t20 = *((unsigned int *)t4);
    t21 = (t19 - t20);
    t22 = (t21 + 1);
    xsi_vlogvar_assign_value(t2, t1, 0, *((unsigned int *)t4), t22);
    goto LAB20;

LAB21:    t19 = *((unsigned int *)t3);
    t20 = *((unsigned int *)t4);
    t21 = (t19 - t20);
    t22 = (t21 + 1);
    xsi_vlogvar_assign_value(t2, t1, 0, *((unsigned int *)t4), t22);
    goto LAB22;

LAB23:    t19 = *((unsigned int *)t3);
    t20 = *((unsigned int *)t4);
    t21 = (t19 - t20);
    t22 = (t21 + 1);
    xsi_vlogvar_assign_value(t2, t1, 0, *((unsigned int *)t4), t22);
    goto LAB24;

}


extern void work_m_00000000002845645633_1114773723_init()
{
	static char *pe[] = {(void *)Always_14_0,(void *)Initial_20_1};
	xsi_register_didat("work_m_00000000002845645633_1114773723", "isim/blram_isim_beh.exe.sim/work/m_00000000002845645633_1114773723.didat");
	xsi_register_executes(pe);
}
