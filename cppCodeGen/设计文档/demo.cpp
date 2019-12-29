enum EnumClassType
{
    Empty_Type = 0,
    ClassType1 ,
    ClassType2
};
class ClassMeta{};
//自定义的sharedptr
typedef SharedPtr<ClassMeta> ClassMetaPtr;
class Class1
{
public:
    Class1();
    Class1(const &Class1 obj );
    Class1& operator=(const &Class1 other);
    ~ Class1();
public:
//some function
public:
 int a;
 float b;
 ClassMeta c;
}
class Class2
{
public:
    Class2();
    Class2(const &Class2 obj );
    Class2& operator=(const &Class2 other);
    ~ Class2();
public:
//some function
public:
 int a;
 float b;
 classMetaPtr c;
}
class ClassName
{
public:
    ClassName();
    ClassName(const &ClassName obj );
    ClassName& operator=(const &ClassName other);
    ~ ClassName();
public:

//some function

public:
    EnumClassType type;
    union
    {
        Class1 class1;
        Class2 class2;
    }
}