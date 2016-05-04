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
static const char *ng0 = "D:/OneDrive/Projects/CS240/lab72/calc_tb.v";
static const char *ng1 = "data";
static const char *ng2 = "result";
static int ng3[] = {1, 0};
static int ng4[] = {0, 0};
static int ng5[] = {20, 0};
static int ng6[] = {2, 0};
static int ng7[] = {10, 0};
static const char *ng8 = "Output Error at time %d, expected %d, received %d, data #%d";
static const char *ng9 = "True Value at time %d, expected %d, received %d, data #%d";
static const char *ng10 = "Design contains no errors";
static const char *ng11 = "Design contains %d errors!";
static int ng12[] = {110, 0};



static void Initial_23_0(char *t0)
{
    char *t1;

LAB0:    xsi_set_current_line(23, ng0);
    t1 = (t0 + 2224);
    xsi_vlogfile_readmemh(ng1, 0, t1, 0, 0, 0, 0);

LAB1:    return;
}

static void Initial_24_1(char *t0)
{
    char *t1;

LAB0:    xsi_set_current_line(24, ng0);
    t1 = (t0 + 2384);
    xsi_vlogfile_readmemh(ng2, 0, t1, 0, 0, 0, 0);

LAB1:    return;
}

static void Initial_26_2(char *t0)
{
    char t4[8];
    char *t1;
    char *t2;
    char *t3;
    char *t5;
    char *t6;
    char *t7;
    unsigned int t8;
    unsigned int t9;
    unsigned int t10;
    unsigned int t11;
    unsigned int t12;
    char *t13;
    char *t14;
    char *t15;
    unsigned int t16;
    unsigned int t17;
    unsigned int t18;
    unsigned int t19;
    unsigned int t20;
    unsigned int t21;
    unsigned int t22;
    unsigned int t23;
    char *t24;

LAB0:    t1 = (t0 + 4600U);
    t2 = *((char **)t1);
    if (t2 == 0)
        goto LAB2;

LAB3:    goto *t2;

LAB2:    xsi_set_current_line(26, ng0);

LAB4:    xsi_set_current_line(27, ng0);
    t2 = ((char*)((ng3)));
    t3 = (t0 + 1584);
    xsi_vlogvar_assign_value(t3, t2, 0, 0, 1);
    xsi_set_current_line(28, ng0);

LAB5:    xsi_set_current_line(29, ng0);
    t2 = (t0 + 4408);
    xsi_process_wait(t2, 5000LL);
    *((char **)t1) = &&LAB6;

LAB1:    return;
LAB6:    xsi_set_current_line(29, ng0);
    t3 = (t0 + 1584);
    t5 = (t3 + 56U);
    t6 = *((char **)t5);
    memset(t4, 0, 8);
    t7 = (t6 + 4);
    t8 = *((unsigned int *)t7);
    t9 = (~(t8));
    t10 = *((unsigned int *)t6);
    t11 = (t10 & t9);
    t12 = (t11 & 1U);
    if (t12 != 0)
        goto LAB10;

LAB8:    if (*((unsigned int *)t7) == 0)
        goto LAB7;

LAB9:    t13 = (t4 + 4);
    *((unsigned int *)t4) = 1;
    *((unsigned int *)t13) = 1;

LAB10:    t14 = (t4 + 4);
    t15 = (t6 + 4);
    t16 = *((unsigned int *)t6);
    t17 = (~(t16));
    *((unsigned int *)t4) = t17;
    *((unsigned int *)t14) = 0;
    if (*((unsigned int *)t15) != 0)
        goto LAB12;

LAB11:    t22 = *((unsigned int *)t4);
    *((unsigned int *)t4) = (t22 & 1U);
    t23 = *((unsigned int *)t14);
    *((unsigned int *)t14) = (t23 & 1U);
    t24 = (t0 + 1584);
    xsi_vlogvar_assign_value(t24, t4, 0, 0, 1);
    goto LAB5;

LAB7:    *((unsigned int *)t4) = 1;
    goto LAB10;

LAB12:    t18 = *((unsigned int *)t4);
    t19 = *((unsigned int *)t15);
    *((unsigned int *)t4) = (t18 | t19);
    t20 = *((unsigned int *)t14);
    t21 = *((unsigned int *)t15);
    *((unsigned int *)t14) = (t20 | t21);
    goto LAB11;

LAB13:    goto LAB1;

}

static void Initial_32_3(char *t0)
{
    char t5[8];
    char *t1;
    char *t2;
    char *t3;
    char *t4;
    char *t6;
    char *t7;
    char *t8;
    char *t9;
    char *t10;
    char *t11;
    char *t12;
    char *t13;
    unsigned int t14;
    unsigned int t15;
    unsigned int t16;
    int t17;
    char *t18;
    char *t19;

LAB0:    t1 = (t0 + 4848U);
    t2 = *((char **)t1);
    if (t2 == 0)
        goto LAB2;

LAB3:    goto *t2;

LAB2:    xsi_set_current_line(32, ng0);

LAB4:    xsi_set_current_line(33, ng0);
    t2 = (t0 + 2224);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t6 = (t0 + 2224);
    t7 = (t6 + 72U);
    t8 = *((char **)t7);
    t9 = (t0 + 2224);
    t10 = (t9 + 64U);
    t11 = *((char **)t10);
    t12 = ((char*)((ng4)));
    xsi_vlog_generic_get_array_select_value(t5, 8, t4, t8, t11, 2, 1, t12, 32, 1);
    t13 = (t0 + 2544);
    xsi_vlogvar_assign_value(t13, t5, 0, 0, 8);
    xsi_set_current_line(34, ng0);
    t2 = ((char*)((ng4)));
    t3 = (t0 + 1744);
    xsi_vlogvar_assign_value(t3, t2, 0, 0, 1);
    xsi_set_current_line(35, ng0);
    t2 = ((char*)((ng4)));
    t3 = (t0 + 1904);
    xsi_vlogvar_assign_value(t3, t2, 0, 0, 1);
    xsi_set_current_line(36, ng0);
    t2 = ((char*)((ng4)));
    t3 = (t0 + 2064);
    xsi_vlogvar_assign_value(t3, t2, 0, 0, 8);
    xsi_set_current_line(37, ng0);
    t2 = ((char*)((ng5)));
    t3 = (t2 + 4);
    t14 = *((unsigned int *)t3);
    t15 = (~(t14));
    t16 = *((unsigned int *)t2);
    t17 = (t16 & t15);
    t4 = (t0 + 7640);
    *((int *)t4) = t17;

LAB5:    t6 = (t0 + 7640);
    if (*((int *)t6) > 0)
        goto LAB6;

LAB7:    xsi_set_current_line(38, ng0);
    t2 = ((char*)((ng3)));
    t3 = (t0 + 1744);
    xsi_vlogvar_wait_assign_value(t3, t2, 0, 0, 1, 1000LL);
    xsi_set_current_line(40, ng0);
    t2 = (t0 + 5680);
    *((int *)t2) = 1;
    t3 = (t0 + 4880);
    *((char **)t3) = t2;
    *((char **)t1) = &&LAB9;

LAB1:    return;
LAB6:    xsi_set_current_line(37, ng0);
    t7 = (t0 + 5664);
    *((int *)t7) = 1;
    t8 = (t0 + 4880);
    *((char **)t8) = t7;
    *((char **)t1) = &&LAB8;
    goto LAB1;

LAB8:    t2 = (t0 + 7640);
    t17 = *((int *)t2);
    *((int *)t2) = (t17 - 1);
    goto LAB5;

LAB9:    xsi_set_current_line(41, ng0);
    t2 = ((char*)((ng4)));
    t3 = (t0 + 1744);
    xsi_vlogvar_wait_assign_value(t3, t2, 0, 0, 1, 1000LL);
    xsi_set_current_line(43, ng0);
    t2 = ((char*)((ng6)));
    t3 = (t2 + 4);
    t14 = *((unsigned int *)t3);
    t15 = (~(t14));
    t16 = *((unsigned int *)t2);
    t17 = (t16 & t15);
    t4 = (t0 + 7644);
    *((int *)t4) = t17;

LAB10:    t6 = (t0 + 7644);
    if (*((int *)t6) > 0)
        goto LAB11;

LAB12:    goto LAB1;

LAB11:    xsi_set_current_line(43, ng0);

LAB13:    xsi_set_current_line(44, ng0);
    t7 = ((char*)((ng4)));
    t8 = (t0 + 2864);
    xsi_vlogvar_assign_value(t8, t7, 0, 0, 32);
    xsi_set_current_line(45, ng0);
    t2 = (t0 + 2544);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t6 = (t4 + 4);
    t14 = *((unsigned int *)t6);
    t15 = (~(t14));
    t16 = *((unsigned int *)t4);
    t17 = (t16 & t15);
    t7 = (t0 + 7648);
    *((int *)t7) = t17;

LAB14:    t8 = (t0 + 7648);
    if (*((int *)t8) > 0)
        goto LAB15;

LAB16:    t2 = (t0 + 7644);
    t17 = *((int *)t2);
    *((int *)t2) = (t17 - 1);
    goto LAB10;

LAB15:    xsi_set_current_line(45, ng0);

LAB17:    xsi_set_current_line(46, ng0);
    t9 = (t0 + 2864);
    t10 = (t9 + 56U);
    t11 = *((char **)t10);
    t12 = ((char*)((ng3)));
    memset(t5, 0, 8);
    xsi_vlog_signed_add(t5, 32, t11, 32, t12, 32);
    t13 = (t0 + 2864);
    xsi_vlogvar_assign_value(t13, t5, 0, 0, 32);
    xsi_set_current_line(47, ng0);
    t2 = (t0 + 2224);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t6 = (t0 + 2224);
    t7 = (t6 + 72U);
    t8 = *((char **)t7);
    t9 = (t0 + 2224);
    t10 = (t9 + 64U);
    t11 = *((char **)t10);
    t12 = (t0 + 2864);
    t13 = (t12 + 56U);
    t18 = *((char **)t13);
    xsi_vlog_generic_get_array_select_value(t5, 8, t4, t8, t11, 2, 1, t18, 32, 1);
    t19 = (t0 + 2064);
    xsi_vlogvar_wait_assign_value(t19, t5, 0, 0, 8, 1000LL);
    xsi_set_current_line(48, ng0);
    t2 = ((char*)((ng3)));
    t3 = (t0 + 1904);
    xsi_vlogvar_wait_assign_value(t3, t2, 0, 0, 1, 1000LL);
    xsi_set_current_line(50, ng0);
    t2 = (t0 + 5696);
    *((int *)t2) = 1;
    t3 = (t0 + 4880);
    *((char **)t3) = t2;
    *((char **)t1) = &&LAB18;
    goto LAB1;

LAB18:    xsi_set_current_line(51, ng0);
    t2 = ((char*)((ng4)));
    t3 = (t0 + 1904);
    xsi_vlogvar_wait_assign_value(t3, t2, 0, 0, 1, 1000LL);
    xsi_set_current_line(52, ng0);
    t2 = ((char*)((ng7)));
    t3 = (t2 + 4);
    t14 = *((unsigned int *)t3);
    t15 = (~(t14));
    t16 = *((unsigned int *)t2);
    t17 = (t16 & t15);
    t4 = (t0 + 7652);
    *((int *)t4) = t17;

LAB19:    t6 = (t0 + 7652);
    if (*((int *)t6) > 0)
        goto LAB20;

LAB21:    t2 = (t0 + 7648);
    t17 = *((int *)t2);
    *((int *)t2) = (t17 - 1);
    goto LAB14;

LAB20:    xsi_set_current_line(52, ng0);
    t7 = (t0 + 5712);
    *((int *)t7) = 1;
    t8 = (t0 + 4880);
    *((char **)t8) = t7;
    *((char **)t1) = &&LAB22;
    goto LAB1;

LAB22:    t2 = (t0 + 7652);
    t17 = *((int *)t2);
    *((int *)t2) = (t17 - 1);
    goto LAB19;

}

static void Initial_59_4(char *t0)
{
    char t5[8];
    char t20[8];
    char t26[16];
    char t31[8];
    char *t1;
    char *t2;
    char *t3;
    char *t4;
    char *t6;
    char *t7;
    char *t8;
    char *t9;
    char *t10;
    char *t11;
    char *t12;
    char *t13;
    unsigned int t14;
    unsigned int t15;
    unsigned int t16;
    int t17;
    char *t18;
    char *t19;
    char *t21;
    char *t22;
    char *t23;
    unsigned int t24;
    unsigned int t25;
    char *t27;
    char *t28;
    char *t29;
    char *t30;
    char *t32;
    char *t33;
    char *t34;
    char *t35;
    char *t36;
    char *t37;
    char *t38;
    char *t39;
    char *t40;
    char *t41;
    char *t42;
    char *t43;
    char *t44;

LAB0:    t1 = (t0 + 5096U);
    t2 = *((char **)t1);
    if (t2 == 0)
        goto LAB2;

LAB3:    goto *t2;

LAB2:    xsi_set_current_line(59, ng0);

LAB4:    xsi_set_current_line(60, ng0);
    t2 = (t0 + 2384);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t6 = (t0 + 2384);
    t7 = (t6 + 72U);
    t8 = *((char **)t7);
    t9 = (t0 + 2384);
    t10 = (t9 + 64U);
    t11 = *((char **)t10);
    t12 = ((char*)((ng4)));
    xsi_vlog_generic_get_array_select_value(t5, 8, t4, t8, t11, 2, 1, t12, 32, 1);
    t13 = (t0 + 2704);
    xsi_vlogvar_assign_value(t13, t5, 0, 0, 8);
    xsi_set_current_line(61, ng0);
    t2 = ((char*)((ng4)));
    t3 = (t0 + 3184);
    xsi_vlogvar_assign_value(t3, t2, 0, 0, 32);
    xsi_set_current_line(62, ng0);
    t2 = ((char*)((ng6)));
    t3 = (t2 + 4);
    t14 = *((unsigned int *)t3);
    t15 = (~(t14));
    t16 = *((unsigned int *)t2);
    t17 = (t16 & t15);
    t4 = (t0 + 7656);
    *((int *)t4) = t17;

LAB5:    t6 = (t0 + 7656);
    if (*((int *)t6) > 0)
        goto LAB6;

LAB7:    xsi_set_current_line(79, ng0);
    t2 = (t0 + 3184);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t6 = ((char*)((ng4)));
    memset(t5, 0, 8);
    xsi_vlog_signed_equal(t5, 32, t4, 32, t6, 32);
    t7 = (t5 + 4);
    t14 = *((unsigned int *)t7);
    t15 = (~(t14));
    t16 = *((unsigned int *)t5);
    t24 = (t16 & t15);
    t25 = (t24 != 0);
    if (t25 > 0)
        goto LAB23;

LAB24:    xsi_set_current_line(82, ng0);
    t2 = (t0 + 3184);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    xsi_vlogfile_write(1, 0, 0, ng11, 2, t0, (char)119, t4, 32);

LAB25:    xsi_set_current_line(84, ng0);
    xsi_vlog_finish(1);

LAB1:    return;
LAB6:    xsi_set_current_line(62, ng0);

LAB8:    xsi_set_current_line(63, ng0);
    t7 = ((char*)((ng4)));
    t8 = (t0 + 3024);
    xsi_vlogvar_assign_value(t8, t7, 0, 0, 32);
    xsi_set_current_line(65, ng0);
    t2 = (t0 + 2704);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t6 = (t4 + 4);
    t14 = *((unsigned int *)t6);
    t15 = (~(t14));
    t16 = *((unsigned int *)t4);
    t17 = (t16 & t15);
    t7 = (t0 + 7660);
    *((int *)t7) = t17;

LAB9:    t8 = (t0 + 7660);
    if (*((int *)t8) > 0)
        goto LAB10;

LAB11:    xsi_set_current_line(76, ng0);
    t2 = (t0 + 5760);
    *((int *)t2) = 1;
    t3 = (t0 + 5128);
    *((char **)t3) = t2;
    *((char **)t1) = &&LAB22;
    goto LAB1;

LAB10:    xsi_set_current_line(65, ng0);
    t9 = (t0 + 5728);
    *((int *)t9) = 1;
    t10 = (t0 + 5128);
    *((char **)t10) = t9;
    *((char **)t1) = &&LAB12;
    goto LAB1;

LAB12:    xsi_set_current_line(65, ng0);

LAB13:    xsi_set_current_line(66, ng0);
    t11 = (t0 + 5744);
    *((int *)t11) = 1;
    t12 = (t0 + 5128);
    *((char **)t12) = t11;
    *((char **)t1) = &&LAB14;
    goto LAB1;

LAB14:    xsi_set_current_line(68, ng0);
    t2 = (t0 + 3024);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t6 = ((char*)((ng3)));
    memset(t5, 0, 8);
    xsi_vlog_signed_add(t5, 32, t4, 32, t6, 32);
    t7 = (t0 + 3024);
    xsi_vlogvar_assign_value(t7, t5, 0, 0, 32);
    xsi_set_current_line(69, ng0);
    t2 = (t0 + 1184U);
    t3 = *((char **)t2);
    t2 = (t0 + 2384);
    t4 = (t2 + 56U);
    t6 = *((char **)t4);
    t7 = (t0 + 2384);
    t8 = (t7 + 72U);
    t9 = *((char **)t8);
    t10 = (t0 + 2384);
    t11 = (t10 + 64U);
    t12 = *((char **)t11);
    t13 = (t0 + 3024);
    t18 = (t13 + 56U);
    t19 = *((char **)t18);
    xsi_vlog_generic_get_array_select_value(t5, 8, t6, t9, t12, 2, 1, t19, 32, 1);
    memset(t20, 0, 8);
    if (*((unsigned int *)t3) != *((unsigned int *)t5))
        goto LAB16;

LAB15:    t21 = (t3 + 4);
    t22 = (t5 + 4);
    if (*((unsigned int *)t21) != *((unsigned int *)t22))
        goto LAB16;

LAB17:    t23 = (t20 + 4);
    t14 = *((unsigned int *)t23);
    t15 = (~(t14));
    t16 = *((unsigned int *)t20);
    t24 = (t16 & t15);
    t25 = (t24 != 0);
    if (t25 > 0)
        goto LAB18;

LAB19:    xsi_set_current_line(73, ng0);
    t2 = xsi_vlog_time(t26, 1000.0000000000000, 1000.0000000000000);
    t3 = (t0 + 2384);
    t4 = (t3 + 56U);
    t6 = *((char **)t4);
    t7 = (t0 + 2384);
    t8 = (t7 + 72U);
    t9 = *((char **)t8);
    t10 = (t0 + 2384);
    t11 = (t10 + 64U);
    t12 = *((char **)t11);
    t13 = (t0 + 3024);
    t18 = (t13 + 56U);
    t19 = *((char **)t18);
    xsi_vlog_generic_get_array_select_value(t5, 8, t6, t9, t12, 2, 1, t19, 32, 1);
    t21 = (t0 + 1184U);
    t22 = *((char **)t21);
    t21 = (t0 + 3024);
    t23 = (t21 + 56U);
    t27 = *((char **)t23);
    xsi_vlogfile_write(1, 0, 0, ng9, 5, t0, (char)118, t26, 64, (char)118, t5, 8, (char)118, t22, 8, (char)119, t27, 32);

LAB20:    t2 = (t0 + 7660);
    t17 = *((int *)t2);
    *((int *)t2) = (t17 - 1);
    goto LAB9;

LAB16:    *((unsigned int *)t20) = 1;
    goto LAB17;

LAB18:    xsi_set_current_line(69, ng0);

LAB21:    xsi_set_current_line(70, ng0);
    t27 = xsi_vlog_time(t26, 1000.0000000000000, 1000.0000000000000);
    t28 = (t0 + 2384);
    t29 = (t28 + 56U);
    t30 = *((char **)t29);
    t32 = (t0 + 2384);
    t33 = (t32 + 72U);
    t34 = *((char **)t33);
    t35 = (t0 + 2384);
    t36 = (t35 + 64U);
    t37 = *((char **)t36);
    t38 = (t0 + 3024);
    t39 = (t38 + 56U);
    t40 = *((char **)t39);
    xsi_vlog_generic_get_array_select_value(t31, 8, t30, t34, t37, 2, 1, t40, 32, 1);
    t41 = (t0 + 1184U);
    t42 = *((char **)t41);
    t41 = (t0 + 3024);
    t43 = (t41 + 56U);
    t44 = *((char **)t43);
    xsi_vlogfile_write(1, 0, 0, ng8, 5, t0, (char)118, t26, 64, (char)118, t31, 8, (char)118, t42, 8, (char)119, t44, 32);
    xsi_set_current_line(71, ng0);
    t2 = (t0 + 3184);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t6 = ((char*)((ng3)));
    memset(t5, 0, 8);
    xsi_vlog_signed_add(t5, 32, t4, 32, t6, 32);
    t7 = (t0 + 3184);
    xsi_vlogvar_assign_value(t7, t5, 0, 0, 32);
    goto LAB20;

LAB22:    t2 = (t0 + 7656);
    t17 = *((int *)t2);
    *((int *)t2) = (t17 - 1);
    goto LAB5;

LAB23:    xsi_set_current_line(80, ng0);
    xsi_vlogfile_write(1, 0, 0, ng10, 1, t0);
    goto LAB25;

}

static void Initial_86_5(char *t0)
{
    char *t1;
    char *t2;
    char *t3;
    unsigned int t4;
    unsigned int t5;
    unsigned int t6;
    int t7;
    char *t8;
    char *t9;
    char *t10;
    char *t11;

LAB0:    t1 = (t0 + 5344U);
    t2 = *((char **)t1);
    if (t2 == 0)
        goto LAB2;

LAB3:    goto *t2;

LAB2:    xsi_set_current_line(86, ng0);

LAB4:    xsi_set_current_line(87, ng0);
    t2 = ((char*)((ng12)));
    t3 = (t2 + 4);
    t4 = *((unsigned int *)t3);
    t5 = (~(t4));
    t6 = *((unsigned int *)t2);
    t7 = (t6 & t5);
    t8 = (t0 + 7664);
    *((int *)t8) = t7;

LAB5:    t9 = (t0 + 7664);
    if (*((int *)t9) > 0)
        goto LAB6;

LAB7:    xsi_set_current_line(88, ng0);
    xsi_vlog_finish(1);

LAB1:    return;
LAB6:    xsi_set_current_line(87, ng0);
    t10 = (t0 + 5776);
    *((int *)t10) = 1;
    t11 = (t0 + 5376);
    *((char **)t11) = t10;
    *((char **)t1) = &&LAB8;
    goto LAB1;

LAB8:    t2 = (t0 + 7664);
    t7 = *((int *)t2);
    *((int *)t2) = (t7 - 1);
    goto LAB5;

}


extern void work_m_00000000001557611430_1175430051_init()
{
	static char *pe[] = {(void *)Initial_23_0,(void *)Initial_24_1,(void *)Initial_26_2,(void *)Initial_32_3,(void *)Initial_59_4,(void *)Initial_86_5};
	xsi_register_didat("work_m_00000000001557611430_1175430051", "isim/calc_tb_isim_beh.exe.sim/work/m_00000000001557611430_1175430051.didat");
	xsi_register_executes(pe);
}
