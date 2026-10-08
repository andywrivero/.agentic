# Worked example: nearest-wins downgrade

All output is real, from Maven 3.6.2 with `maven-dependency-plugin` 3.6.1 and `maven-enforcer-plugin` 3.4.1.

The project declares `commons-codec` 1.6 directly and `httpclient` 4.5.14, which needs `commons-codec` 1.11.

## Diagnose

`mvn dependency:tree -Dverbose`:

```
com.example:style:jar:1.0-SNAPSHOT
+- commons-codec:commons-codec:jar:1.6:compile
\- org.apache.httpcomponents:httpclient:jar:4.5.14:compile
   +- org.apache.httpcomponents:httpcore:jar:4.4.16:compile
   +- commons-logging:commons-logging:jar:1.2:compile
   \- (commons-codec:commons-codec:jar:1.11:compile - omitted for conflict with 1.6)
```

The direct declaration is nearer to the root, so Maven puts 1.6 on the classpath. `httpclient` then runs against an older codec than it was built for, which can fail at runtime with `NoSuchMethodError`.

`mvn enforcer:enforce -Denforcer.rules=requireUpperBoundDeps` catches it:

```
Require upper bound dependencies error for commons-codec:commons-codec:1.6 paths to dependency are:
+-com.example:style:1.0-SNAPSHOT
  +-commons-codec:commons-codec:1.6
and
+-com.example:style:1.0-SNAPSHOT
  +-org.apache.httpcomponents:httpclient:4.5.14
    +-commons-codec:commons-codec:1.11
```

## Fix

Declare the version once, in `dependencyManagement`, at the highest version any path needs, and remove the version from the direct declaration:

```xml
<properties>
    <commons-codec.version>1.11</commons-codec.version>
</properties>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>commons-codec</groupId>
            <artifactId>commons-codec</artifactId>
            <version>${commons-codec.version}</version>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <dependency>
        <groupId>commons-codec</groupId>
        <artifactId>commons-codec</artifactId>
    </dependency>
    <!-- httpclient unchanged -->
</dependencies>
```

## Verify

```
+- commons-codec:commons-codec:jar:1.11:compile
\- org.apache.httpcomponents:httpclient:jar:4.5.14:compile
   ...
   \- (commons-codec:commons-codec:jar:1.11:compile - version managed from 1.11; omitted for duplicate)
```

```
Rule 0: org.apache.maven.enforcer.rules.dependency.RequireUpperBoundDeps passed
BUILD SUCCESS
```

Then run `./mvnw -q verify`, because code that used 1.6 APIs must still compile and pass against 1.11.
