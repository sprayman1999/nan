; ModuleID = 'test.nan'
source_filename = "test.nan"
target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
@.str.1 = private unnamed_addr constant [14 x i8] c"this is main!\00", align 1
@.str.0 = private unnamed_addr constant [18 x i8] c"call Hello World!\00", align 1
define i32 @hello_world() #0 {
    call i32 @puts(i8* getelementptr inbounds ([18 x i8], [18 x i8]* @.str.0, i64 0, i64 0))

    ret i32 0
}

define i32 @main() #1 {
    call i32 @hello_world()
    call i32 @puts(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str.1, i64 0, i64 0))

    ret i32 0
}

declare i32 @puts(i8*) #1

